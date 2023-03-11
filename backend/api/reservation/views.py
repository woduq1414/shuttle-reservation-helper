from fastapi import APIRouter, FastAPI, Depends, Request
from sqlalchemy.orm import Session

from models import Reservation
from dependency import get_db, get_schedule_id, init_schedule
from datetime import datetime, timedelta

from scheduler import scheduler

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get("/list")
async def get_reservation_list(db: Session = Depends(get_db)):
    now = datetime.now()
    target_date = now + timedelta(days=2)
    target_date = datetime(target_date.year, target_date.month, target_date.day, 0, 0, 0)

    return [{"seq": x.seq, "departure": x.departure, "departure_time": x.departure_time, "arrival_time": x.arrival_time,
             "shuttle_date": x.shuttle_date.strftime("%Y%m%d")} for x in
            db.query(Reservation).filter(Reservation.shuttle_date >= target_date).order_by(
                Reservation.shuttle_date).all()]


@router.post("/")
async def make_reservation(payload: Request, db: Session = Depends(get_db)):
    payload = await payload.json()
    print(payload)

    reservation_row = Reservation(
        departure=payload["departure"],
        departure_time=payload["departure_time"],
        arrival_time=payload["arrival_time"],
        shuttle_date=datetime(int(payload["shuttle_date"][:4]), int(payload["shuttle_date"][4:6]),
                              int(payload["shuttle_date"][6:8])),
        add_datetime=datetime.now()
    )
    db.add(reservation_row)
    db.commit()

    init_schedule()

    return "success"


@router.delete("/")
async def delete_reservation(seq: int, db: Session = Depends(get_db)):
    print(seq)
    target_row = db.query(Reservation).filter(Reservation.seq == seq).first()

    sched_id = get_schedule_id(target_row)
    try:
        scheduler.remove_job(sched_id)
    except:
        pass
    db.delete(target_row)
    db.commit()

    return "success"
