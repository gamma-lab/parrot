from flask import jsonify, request
from ..model import UserSaysExample, UserSaysExampleEntityAssociation
from . import api
from .. import db


@api.route('/user_says_examples', methods=['POST'])
def create_user_says_example():
    user_says_example = UserSaysExample(
        content=request.json.get('content')
    )
    db.session.add(user_says_example)
    try:
        db.session.commit()
        return jsonify(user_says_example.to_json()), 201
    except Exception as e:
        print(e)
        db.session.rollback()
        return 'Bad request', 400


@api.route('/user_says_examples/<int:user_says_example_id>', methods=['PUT'])
def update_user_says_example(user_says_example_id):
    user_says_example = UserSaysExample.query.get(user_says_example_id)
    if user_says_example:
        user_says_example.content = request.json.get('content')
        db.session.add(user_says_example)
        try:
            db.session.commit()
            return jsonify(user_says_example.to_json())
        except Exception as e:
            return 'Bad request', 400
    else:
        return 'Not Found', 404


@api.route('/user_says_examples/<int:user_says_example_id>',
           methods=['DELETE'])
def delete_user_says_example(user_says_example_id):
    user_says_example = UserSaysExample.query.get(user_says_example_id)
    if user_says_example:
        db.session.delete(user_says_example)
        try:
            db.session.commit()
            return 'Success', 204
        except Exception as e:
            return 'Bad request', 400
    else:
        return 'Not Found', 404


@api.route('/user_says_examples/<int:user_says_example_id>/entity_annotate',
           methods=['POST'])
def create_entity_annotation(user_says_example_id):
    user_says_example = UserSaysExample.query.get(user_says_example_id)
    if user_says_example:
        # print(request.json)
        annotation = UserSaysExampleEntityAssociation(
            user_says_example_id=user_says_example_id,
            entity_id=request.json.get('entity_id'),
            value=request.json.get('value'),
            start_index=request.json.get('start_index'),
            end_index=request.json.get('end_index')
        )
        db.session.add(annotation)
        try:
            db.session.commit()
            return jsonify(annotation.annotated_content()), 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return 'Bad request', 400
    else:
        return 'Not Found', 404


@api.route(
    '/user_says_examples/<int:user_says_example_id>/entity_annotate/<int:annotation_id>',
    methods=['PUT'])
def update_entity_annotation(user_says_example_id, annotation_id):
    annotation = UserSaysExampleEntityAssociation.query.filter_by(
        user_says_example_id=user_says_example_id,
        id=annotation_id
    ).first()
    if annotation:
        # print(request.json)
        annotation.entity_id = request.json.get('entity_id')
        db.session.add(annotation)
        try:
            db.session.commit()
            return jsonify(annotation.annotated_content()), 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return 'Bad request', 400
    else:
        return 'Not Found', 404
