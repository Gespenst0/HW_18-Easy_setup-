from flask import jsonify
from flask_restx import Namespace, Resource

from app.models import Director,Director_Schema

directors_ns = Namespace('directors')

@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        director_schema = Director_Schema(many=True)
        directors = Director.query.all()
        if not directors:
            return "", 404
        return jsonify(director_schema.dump(directors))


@directors_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did):
        director_schema = Director_Schema()
        director = Director.query.get(did)
        if not director:
            return "", 404
        return jsonify(director_schema.dump(director))