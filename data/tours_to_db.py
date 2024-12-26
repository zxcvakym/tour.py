from data.base import Session
from data import data
from data.models import Tour


def data_to_db():
    with Session() as session:
        for index, tour in data.tours.items():
            tour_db = Tour(id=index, **tour)
            session.add(tour_db)

        session.commit()