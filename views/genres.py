from flask import jsonify
from flask_restx import Namespace, Resource
from app.utils import get_movies_by_genre
from app.models import Genre, GenreSchema

genres_ns = Namespace('genres')


@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        genre_schema = GenreSchema(many=True)
        genres = Genre.query.all()
        if not genres:
            return "", 404
        return jsonify(genre_schema.dump(genres))


@genres_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid):
        genre_schema = GenreSchema()
        genre = Genre.query.get(gid)
        if not genre:
            return "", 404
        movies = get_movies_by_genre(gid)
        list_titles = []
        for movie in movies:
            list_titles.append(movie["title"])
        if len(list_titles) == 0:
            list_titles = "Movies not found"
        result = genre_schema.dump(genre)
        result["Titles"] = list_titles
        return jsonify(result)
