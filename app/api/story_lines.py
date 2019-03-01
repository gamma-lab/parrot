from flask import jsonify, request
from ..model import StoryLine
from . import api
from .. import db


@api.route('/story_lines', methods=['POST'])
def create_story_line():
    story_line = StoryLine(
        position=request.json.get('position'),
        story_id=request.json.get('story_id')
    )
    # story_line.intent = []
    # story_line.actions = []
    db.session.add(story_line)
    try:
        db.session.commit()
        return jsonify(story_line.to_json()), 201
    except Exception as e:
        db.session.rollback()
        return 'Bad request', 400


@api.route('/stories/<int:story_line_id>')
def get_story_line(story_line_id):
    story_line = StoryLine.query.get(story_line_id)
    if story_line:
        return jsonify(story_line.to_json())
    else:
        return 'Bad request', 400
