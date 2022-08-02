from config import movies_schema, db
from models import Movie


def insert_data_to_db(data):
    list_data = []
    for item in movies_schema.load(data):
        list_data.append(Movie(**item))
    with db.session.begin():
        db.session.add_all(list_data)