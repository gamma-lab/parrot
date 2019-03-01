from flask import jsonify, request
from ..model import Intent
from . import api
from .. import db


@api.route('/intents', methods=['POST'])
def create_intent():
    intent = Intent(
        intent_name=request.json.get('intentName'),
        domain_id=request.json.get('domainId'),
        user_says=""
    )
    db.session.add(intent)
    try:
        db.session.commit()
        return jsonify(intent.to_json()), 201
    except Exception as e:
        db.session.rollback()
        return 'Bad request', 400


@api.route('/intents/<int:intent_id>')
def get_intent(intent_id):
    intent = Intent.query.get(intent_id)
    if intent:
        return jsonify(intent.to_json())
    else:
        return 'Bad request', 400


@api.route('/intents/<int:intent_id>', methods=['PUT'])
def update_intent(intent_id):
    intent = Intent.query.get(intent_id)
    if intent:
        intent.intent_name = request.json.get('intentName')
        intent.user_says = request.json.get('userSays')
        db.session.add(intent)
        try:
            db.session.commit()
            return jsonify(intent.to_json())
        except Exception as e:
            return 'Bad request', 400
    else:
        return 'Not Found', 404


@api.route('/intents/<int:intent_id>', methods=['DELETE'])
def delete_intent(intent_id):
    intent = Intent.query.get(intent_id)
    if intent:
        db.session.delete(intent)
        try:
            db.session.commit()
            return 'success', 200
        except Exception as e:
            return 'Bad request', 400
    else:
        return 'Not Found', 404
