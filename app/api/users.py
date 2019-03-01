from flask import jsonify, request
from ..model import User
from . import api
from .. import db


@api.route('/users', methods=['POST'])
def create_user():
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    email = request.json.get('email')
    password = request.json.get('password')
    user = User(first_name=first_name,
                last_name=last_name,
                email=email,
                password=password)
    db.session.add(user)
    try:
        db.session.commit()
        return jsonify(user.to_json()), 201
    except Exception as e:
        db.session.rollback()
        return 'Bad request', 400


@api.route('/users')
def all_users():
    users = [user.to_json() for user in User.query.all()]
    return jsonify(users)


@api.route('/users/<int:user_id>')
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.to_json())
    else:
        return 'Bad request', 400
