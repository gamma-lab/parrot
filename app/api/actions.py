from flask import jsonify, request
from ..model import Action
from . import api
from .. import db


@api.route('/actions', methods=['POST'])
def create_action():
    action = Action(
        action_name=request.json.get('actionName'),
        domain_id=request.json.get('domainId')
    )
    db.session.add(action)
    try:
        db.session.commit()
        return jsonify(action.to_json()), 201
    except Exception as e:
        print(e)
        db.session.rollback()
        return 'Bad request', 400


@api.route('/actions/<int:action_id>')
def get_action(action_id):
    action = Action.query.get(action_id)
    if action:
        return jsonify(action.to_json())
    else:
        return 'Bad request', 400


@api.route('/actions/<int:action_id>', methods=['PUT'])
def update_action(action_id):
    action = Action.query.get(action_id)
    if action:
        action.action_name = request.json.get('actionName')
        action.agent_responses = request.json.get('agentResponses')
        db.session.add(action)
        try:
            db.session.commit()
            return jsonify(action.to_json())
        except Exception as e:
            return 'Bad request', 400
    else:
        return 'Not Found', 404


@api.route('/actions/<int:action_id>', methods=['DELETE'])
def delete_action(action_id):
    action = Action.query.get(action_id)
    if action:
        db.session.delete(action)
        try:
            db.session.commit()
            return 'success', 200
        except Exception as e:
            return 'Bad request', 400
    else:
        return 'Not Found', 404
