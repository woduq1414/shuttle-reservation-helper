from datetime import timedelta, datetime

from db import SessionLocal

import json

import requests
from urllib import parse

from bs4 import BeautifulSoup  # parser

from jsbn import RSAKey

from models import Reservation

from scheduler import scheduler

default_headers = {
    'Accept': '*/*',
    'Accept-Language': 'ko,ko-KR;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://underwood1.yonsei.ac.kr',
    'Referer': 'https://underwood1.yonsei.ac.kr/com/lgin/SsoCtr/initExtPageWork.do?link=shuttle',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_portal_login_cookie():
    #
    # user defined
    import config as cf

    with requests.Session() as s:
        #
        # Step 1. Generate cookie.
        res = s.get(cf.NYSCEC_LOGIN_INDEX)

        #
        # Step 2. Use cookie to get S1 parameter
        request_payload = {
            "retUrl": cf.NYSCEC_BASE,
            "failUrl": cf.NYSCEC_BASE,
            "ssoGubun": "Redirect",
            "returnUrl": "L2NvbS9sZ2luL1Nzb0N0ci9pbml0RXh0UGFnZVdvcmsuZG8/bGluaz1zaHV0dGxl",
            "locale": "ko"
        }

        res = s.post(
            cf.NYSCEC_SPLOGIN, request_payload,
            cookies=res.cookies.get_dict())

        #
        # Step 3. Request keyModulus and key Exponent
        soup = BeautifulSoup(res.text, 'html.parser')
        request_payload = {
            "app_id": cf.APP_ID,
            "retUrl": cf.NYSCEC_BASE,
            "failUrl": cf.NYSCEC_BASE,
            "baseUrl": cf.NYSCEC_BASE,
            "S1": str(soup.find('input', id='S1').get('value')),
            "loginUrl": '',
            "ssoGubun": "Redirect",
            "refererUrl": cf.NYSCEC_LOGIN_INDEX,
            "a": "aaaa",
            "b": "bbbb",
            "returnUrl": "L2NvbS9sZ2luL1Nzb0N0ci9pbml0RXh0UGFnZVdvcmsuZG8/bGluaz1zaHV0dGxl",
            "locale": "ko"
        }

        res = s.post(
            cf.NYSCEC_PMSSO_SERVICE,
            request_payload)

        # Step 4. Second reqeust to index page

        ssoChallenge = res.text.split('ssoChallenge= \'')[1].split('\';')[0]
        keyModulus = res.text.split('rsa.setPublic( \'')[1].split('\',')[0]
        keyExponent = res.text.split('rsa.setPublic( \'' + keyModulus + '\', \'')[1].split('\' );')[0]

        # Generate E2 value
        jsonObj = {
            'userid': cf.NYSCEC_LOGIN_PARAM['username'],
            'userpw': cf.NYSCEC_LOGIN_PARAM['password'],
            'ssoChallenge': ssoChallenge
        }

        rsa = RSAKey()
        rsa.setPublic(
            keyModulus,
            keyExponent
        )

        E2 = rsa.encrypt(json.dumps(jsonObj))

        request_payload = {
            "app_id": cf.APP_ID,
            "retUrl": cf.NYSCEC_BASE,
            "failUrl": cf.NYSCEC_BASE,
            "baseUrl": cf.NYSCEC_BASE,
            "loginUrl": '',
            "loginType": "invokeID",
            "ssoGubun": "Redirect",
            "refererUrl": cf.NYSCEC_LOGIN_INDEX,
            "E2": E2,
            "E3": "",
            "E4": "",
            "a": "aaaa",
            "b": "bbbb",
            "loginId": '',
            "loginPassword": '',
            "returnUrl": "L2NvbS9sZ2luL1Nzb0N0ci9pbml0RXh0UGFnZVdvcmsuZG8/bGluaz1zaHV0dGxl",
            "locale": "ko"
        }

        res = s.post(
            cf.NYSCEC_PMSSOAUTH_SERVICE,
            request_payload)

        soup = BeautifulSoup(res.text, 'html.parser')

        request_payload = {
            "app_id": cf.APP_ID,
            "retUrl": cf.NYSCEC_BASE,
            "failUrl": cf.NYSCEC_BASE,
            "baseUrl": cf.NYSCEC_BASE,
            "loginUrl": '',
            "E3": str(soup.find('input', id='E3').get('value')),
            "E4": str(soup.find('input', id='E4').get('value')),
            "S2": str(soup.find('input', id='S2').get('value')),
            "CLTID": str(soup.find('input', id='CLTID').get('value')),
            "refererUrl": cf.NYSCEC_LOGIN_INDEX,
            "ssoGubun": "Redirect",
            "a": "aaaa",
            "b": "bbbb",
            "returnUrl": "L2NvbS9sZ2luL1Nzb0N0ci9pbml0RXh0UGFnZVdvcmsuZG8/bGluaz1zaHV0dGxl",
            "locale": "ko"
        }

        res = s.post(
            cf.NYSCEC_SPLOGIN_DATA,
            request_payload)

        s.get(cf.NYSCEC_SPLOGIN_PROCESS)

        return s.cookies.get_dict()


def do_reservation(cookies, departure, date, departure_time, arrival_time=None):
    with requests.Session() as s:

        s.cookies = requests.utils.cookiejar_from_dict(cookies)
        url = "https://underwood1.yonsei.ac.kr/sch/shtl/ShtlrmCtr/findShtlbusResveList.do"

        payload = f"_menuId=MTA3NDkwNzI0MDIyNjk1MTQwMDA%3D&_menuNm=&_pgmId=MzI5MzAyNzI4NzE%3D&%40d1%23areaDivCd={departure}&%40d1%23stdrDt={date}&%40d1%23resvePosblDt=2&%40d1%23seatDivCd=1&%40d1%23areaDivCd2=&%40d1%23stdrDt2={datetime.now().strftime('%Y%m%d')}&%40d1%23userDivCd=12&%40d%23=%40d1%23&%40d1%23=dmCond&%40d1%23tp=dm&"
        print(payload)
        response = s.post(url, data=payload, headers=default_headers)

        shuttle_data = json.loads(response.text)["dsShtl110"]
        print(response.text)
        print(shuttle_data)
        target_shuttle = [x for x in shuttle_data if x["beginTm"] == departure_time][0]
        print(target_shuttle)
        url = "https://underwood1.yonsei.ac.kr/sch/shtl/ShtlrmCtr/saveShtlbusResveList.do"

        # payload = {'_findSavedRow': 'areaDivCd, busCd, seatNo, stdrDt, beginTm',
        #            '_menuId': 'MTA3NDkwNzI0MDIyNjk1MTQwMDA',
        #            '_menuNm': '', '_pgmId': 'MzI5MzAyNzI4NzE', '@d1#areaDivCd': 'S', '@d1#busCd': 'S4',
        #            '@d1#busNm': '4호차',
        #            '@d1#seatNo': '', '@d1#stdrDt': '20230303', '@d1#beginTm': '0830', '@d1#endTm': '0930',
        #            '@d1#tm': '08:30 ~ 09:30', '@d1#seatDivCd': '', '@d1#userDivCd': '', '@d1#persNo': '',
        #            '@d1#thrstNm': '영종대교, 인천대교', '@d1#remrk': '', '@d1#remndSeat': '14', '@d1#resveWaitPcnt': '5',
        #            '@d1#resveYn': '0', '@d1#resveWaitYn': '0', '@d1#resveResnDivCd': '4', '@d1#dailResvePosblYn': '1',
        #            '@d1#areaDivCd__origin': 'S', '@d1#busCd__origin': target_shuttle["busCd"], '@d1#seatNo__origin': '',
        #            '@d1#stdrDt__origin': '20230303', '@d1#beginTm__origin': departure_time, '@d1#sts': 'u',
        #            '@d#': '@d2#',
        #            '@d1#': 'dsShtl110', '@d1#tp': 'ds', '@d2#gbn': 'P', '@d2#seatDivCd': '1', '@d2#userDivCd': '12',
        #            '@d2#': 'dmCond', '@d2#tp': 'dm',}

        payload = {'_findSavedRow': 'areaDivCd, busCd, seatNo, stdrDt, beginTm',
                   '_menuId': 'MTA3NDkwNzI0MDIyNjk1MTQwMDA=',
                   '_menuNm': '', '_pgmId': 'MzI5MzAyNzI4NzE=', '@d1#areaDivCd': 'S', '@d1#busCd': 'S4',
                   '@d1#busNm': '4호차',
                   '@d1#seatNo': '', '@d1#stdrDt': '20230303', '@d1#beginTm': '0830', '@d1#endTm': '0930',
                   '@d1#tm': '08:30 ~ 09:30', '@d1#seatDivCd': '', '@d1#userDivCd': '', '@d1#persNo': '',
                   '@d1#thrstNm': '영종대교, 인천대교', '@d1#remrk': '', '@d1#remndSeat': '14', '@d1#resveWaitPcnt': '5',
                   '@d1#resveYn': '0', '@d1#resveWaitYn': '0', '@d1#resveResnDivCd': '4', '@d1#dailResvePosblYn': '1',
                   '@d1#areaDivCd__origin': 'S', '@d1#busCd__origin': "S4", '@d1#seatNo__origin': '',
                   '@d1#stdrDt__origin': '20230303', '@d1#beginTm__origin': "0830", '@d1#sts': 'u',
                   '@d#': '@d1#',
                   '@d1#': 'dsShtl110', '@d1#tp': 'ds', '@d2#gbn': 'P', '@d2#seatDivCd': '1', '@d2#userDivCd': '12',
                   '@d2#': 'dmCond', '@d2#tp': 'dm', }

        for k, v in target_shuttle.items():
            if v is not None:

                payload[f'@d1#{k}'] = str(v)
            else:
                payload[f'@d1#{k}'] = ''

        # payload['@d#']= '@d1#'
        payload = [f'{k}={v.replace("=", "%3D")}' for k, v in payload.items()]

        payload = parse.quote('&'.join(payload), safe='%=&') + "&%40d%23=%40d2%23&"

        response = s.post(url, payload, headers=default_headers)

        print(response.text)


def login_and_reservation(departure, date, departure_time):
    print(departure, date, departure_time)
    if departure == "신촌":
        departure = "S"
    elif departure == "국제":
        departure = "I"

    retry = 0
    try:

        if retry >= 3:
            return
        retry += 1

        cookies = get_portal_login_cookie()

        do_reservation(cookies, departure, date, departure_time)

    except:
        pass


def init_schedule():
    db = next(get_db())

    now = datetime.now()
    # target_date = now - timedelta(days=2)
    target_date = now + timedelta(days=2)
    target_date = datetime(target_date.year, target_date.month, target_date.day, 14, 1, 0)

    reservation_list = db.query(Reservation).order_by(
        Reservation.shuttle_date).all()

    for reservation_row in reservation_list:

        if reservation_row.shuttle_date < target_date:
            try:
                scheduler.remove_job(get_schedule_id(reservation_row))
            except:
                pass
            db.delete(reservation_row)
            continue

        target_date = reservation_row.shuttle_date - timedelta(days=2)
        target_date = datetime(target_date.year, target_date.month, target_date.day, 14, 1, 0)
        scheduler.add_job(login_and_reservation, 'date', id=get_schedule_id(reservation_row), run_date=target_date,
                          args=[reservation_row.departure, reservation_row.shuttle_date,
                                reservation_row.departure_time], replace_existing=True)

        print(target_date, get_schedule_id(reservation_row))

    db.commit()
    # print([x.shuttle_date for x in reservation_list])


def get_schedule_id(res_row):
    return f'{res_row.departure}_{res_row.shuttle_date}_{res_row.departure_time}'


if __name__ == "__main__":
    print(init_schedule())
    cookies = get_portal_login_cookie()

    do_reservation(cookies, "S", "20230321", "1230", "0820")
