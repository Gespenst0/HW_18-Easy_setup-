from flask import jsonify, request
from flask_restx import Namespace, Resource
from app.models import Movie, MovieSchema
from app.setup_db import db
from app.utils import get_movies_by_both_parameters, get_movies_by_genre, get_movies_by_director, get_movies_by_year

movies_ns = Namespace('movies')


@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get("director_id")
        genre_id = request.args.get("genre_id")
        year = request.args.get("year")
        if year:
            return jsonify(get_movies_by_year(year))
        elif director_id and genre_id:
            return get_movies_by_both_parameters(director_id, genre_id)
        elif director_id:
            return get_movies_by_director(director_id)
        elif genre_id:
            return jsonify(get_movies_by_genre(genre_id))
        else:
            return get_movies_by_director(director_id)

    def post(self):
        req_json = request.json()
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return "", 201


@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid):
        movieSchema = MovieSchema()
        movie = Movie.query.get(mid)
        if not movie:
            return "", 404
        return jsonify(movieSchema.dump(movie))

    def put(self, mid: int):
        movie = Movie.query.get(mid)
        if not movie:
            return "", 404
        req_json = request.json
        movie.title = req_json.get("title")
        movie.description = req_json.get("description")
        movie.trailer = req_json.get("trailer")
        movie.year = req_json.get("year")
        movie.rating = req_json.get("rating")
        movie.genre_id = req_json.get("genre_id")
        movie.director_id = req_json.get("director_id")
        db.session.add(movie)
        db.session.commit()
        return "", 204

    def patch(self, mid: int):
        movie = Movie.query.get(mid)
        if not movie:
            return "", 404
        req_json = request.json
        if "title" in req_json:
            movie.title = req_json.get("title")
        if "description" in req_json:
            movie.description = req_json.get("description")
        if "trailer" in req_json:
            movie.trailer = req_json.get("trailer")
        if "year" in req_json:
            movie.year = req_json.get("year")
        if "rating" in req_json:
            movie.rating = req_json.get("rating")
        if "genre_id" in req_json:
            movie.genre_id = req_json.get("genre_id")
        if "director_id" in req_json:
            movie.director_id = req_json.get("director_id")
        db.session.add(movie)
        db.session.commit()
        return "", 204

    def delete(self, mid: int):
        movie = Movie.query.get(mid)
        if not movie:
            return "", 404
        db.session.delete(movie)
        db.session.commit()
        return "", 204
