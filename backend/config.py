import json

NYSCEC_LOGIN_PARAM = {
    'username': '',
    'password': ''
}



with open("secret.json", 'r') as file:
    data = json.load(file)
    NYSCEC_LOGIN_PARAM['username'] = data['username']
    NYSCEC_LOGIN_PARAM['password'] = data['password']



NYSCEC_LOGIN_PARAM = {
    'username': '2022149002',
    'password': 'woduq1219!'
}



APP_ID = "haksaYonsei"
NYSCEC_BASE = 'https://underwood1.yonsei.ac.kr:443'
NYSCEC_LOGIN_INDEX = 'https://underwood1.yonsei.ac.kr/passni/spLogin.jsp?returnUrl=L2NvbS9sZ2luL1Nzb0N0ci9pbml0RXh0UGFnZVdvcmsuZG8/bGluaz1zaHV0dGxl&locale=ko'

NYSCEC_SPLOGIN = 'https://underwood1.yonsei.ac.kr/SSOLegacy.do'
NYSCEC_SPLOGIN_DATA = 'https://underwood1.yonsei.ac.kr/SSOLegacy.do?pname=spLoginData'
NYSCEC_SPLOGIN_PROCESS = 'https://underwood1.yonsei.ac.kr/com/lgin/SsoCtr/j_login_sso.do'

NYSCEC_PMSSO_SERVICE = 'https://infra.yonsei.ac.kr/sso/PmSSOService'
NYSCEC_PMSSOAUTH_SERVICE = 'https://infra.yonsei.ac.kr/sso/PmSSOAuthService'
