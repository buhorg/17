from flask import jsonify, request
from flask_restx import Resource

from config import db, movie_schema, movie_ns, app, movies_schema, director_ns, genre_ns, directors_schema, \
    director_schema, genre_schema, genres_schema
from models import Movie, Director, Genre
from utils import insert_data_to_db


@movie_ns.route('/')
class MovieView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        if (director_id is None) and (genre_id is None):
            all_movies = db.session.query(Movie).all()
            return jsonify(movies_schema.dump(all_movies))
        elif (director_id is not None) and (genre_id is None):
            movies = db.session.query(Movie).filter(Movie.director_id == director_id).all()
            return jsonify(movies_schema.dump(movies))
        elif (director_id is None) and (genre_id is not None):
            movies = db.session.query(Movie).filter(Movie.genre_id == genre_id).all()
            return jsonify(movies_schema.dump(movies))
        else:
            movies = db.session.query(Movie).filter(Movie.genre_id == genre_id, Movie.director_id == director_id).all()
            return jsonify(movies_schema.dump(movies))

    def post(self):
        request_json = request.json
        if isinstance(request_json, list):
            insert_data_to_db(request_json)
        elif isinstance(request_json, dict):
            insert_data_to_db([request_json])
        else:
            return "Не верный тип данных для вставки"
        return "", 201


@movie_ns.route('/<int:uid>')
class MovieView(Resource):
    def get(self, uid):
        movie = db.session.query(Movie).get_or_404(uid)
        return movie_schema.dump(movie), 200

    def put(self, uid):
        db.session.query(Movie).filter(Movie.id == uid).update(request.json)
        db.session.commit()
        return "", 204

    def delete(self, uid):
        delete_rows = db.session.query(Movie).filter(Movie.id == uid).delete()
        if delete_rows == 0:
            return None, 404
        db.session.commit()
        return "", 204


@director_ns.route('/')
class DirectorView(Resource):
    def get(self):
        directors = db.session.query(Director).all()
        return jsonify(directors_schema.dump(directors))


@director_ns.route('/<int:uid>')
class DirectorView(Resource):
    def get(self, uid):
        director = db.session.query(Director).get_or_404(uid)
        return director_schema.dump(director), 200


@genre_ns.route('/')
class GenreView(Resource):
    def get(self):
        genres = db.session.query(Genre).all()
        return jsonify(genres_schema.dump(genres))


@genre_ns.route('/<int:uid>')
class GenreView(Resource):
    def get(self, uid):
        genre = db.session.query(Genre).get_or_404(uid)
        return genre_schema.dump(genre), 200


if __name__ == '__main__':
    app.run(debug=True)
