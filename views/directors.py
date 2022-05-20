from flask import jsonify
from flask_restx import Namespace, Resource
from app.models import Director, DirectorSchema

directors_ns = Namespace('directors')


@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        director_schema = DirectorSchema(many=True)
        directors = Director.query.all()
        if not directors:
            return "", 404
        return jsonify(director_schema.dump(directors))


@directors_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did):
        director_schema = DirectorSchema()
        director = Director.query.get(did)
        if not director:
            return "", 404
        return jsonify(director_schema.dump(director))
