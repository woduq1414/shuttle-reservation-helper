from fastapi import APIRouter, FastAPI

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get("/list")
async def list():
    shuttle_list_data = {
        "신촌": [
            {"departure_time": "07:00", "arrival_time": "08:00"},
            {"departure_time": "07:20", "arrival_time": "08:20"},
            {"departure_time": "07:40", "arrival_time": "08:40"},
            {"departure_time": "08:30", "arrival_time": "09:30"},
            {"departure_time": "09:30", "arrival_time": "10:30"},
            {"departure_time": "10:30", "arrival_time": "11:30"},
            {"departure_time": "11:30", "arrival_time": "12:30"},
            {"departure_time": "12:30", "arrival_time": "13:30"},
            {"departure_time": "14:30", "arrival_time": "15:30"},
            {"departure_time": "15:10", "arrival_time": "16:10"},
            {"departure_time": "16:30", "arrival_time": "17:30"},
            {"departure_time": "17:10", "arrival_time": "18:10"},
            {"departure_time": "17:30", "arrival_time": "18:30"},
            {"departure_time": "18:10", "arrival_time": "19:10"},
            {"departure_time": "18:30", "arrival_time": "19:30"},
            {"departure_time": "19:00", "arrival_time": "20:00"},
            {"departure_time": "20:00", "arrival_time": "21:00"},
            {"departure_time": "21:00", "arrival_time": "22:00"},

        ],
        "국제": [
            {"departure_time": "07:00", "arrival_time": "08:00"},
            {"departure_time": "07:20", "arrival_time": "08:20"},
            {"departure_time": "07:40", "arrival_time": "08:40"},
            {"departure_time": "08:30", "arrival_time": "09:30"},
            {"departure_time": "09:30", "arrival_time": "10:30"},
            {"departure_time": "10:30", "arrival_time": "11:30"},
            {"departure_time": "11:30", "arrival_time": "12:30"},
            {"departure_time": "12:30", "arrival_time": "13:30"},
            {"departure_time": "14:30", "arrival_time": "15:30"},
            {"departure_time": "15:10", "arrival_time": "16:10"},
            {"departure_time": "16:30", "arrival_time": "17:30"},
            {"departure_time": "17:10", "arrival_time": "18:10"},
            {"departure_time": "17:30", "arrival_time": "18:30"},
            {"departure_time": "18:10", "arrival_time": "19:10"},
            {"departure_time": "18:30", "arrival_time": "19:30"},
            {"departure_time": "19:00", "arrival_time": "20:00"},
            {"departure_time": "19:40", "arrival_time": "20:40"},
            {"departure_time": "20:00", "arrival_time": "21:00"},

        ]
    }

    return shuttle_list_data
