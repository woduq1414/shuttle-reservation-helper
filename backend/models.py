from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship


from db import Base


class Reservation(Base):
    __tablename__ = "reservation"

    seq = Column(Integer, primary_key=True, index=True, autoincrement=True)

    departure = Column(String, nullable=False)
    departure_time = Column(String, nullable=False)
    arrival_time = Column(String, nullable=False)

    shuttle_date = Column(DateTime, nullable=False)

    add_datetime = Column(DateTime, nullable=False)


