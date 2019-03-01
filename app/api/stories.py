from flask import jsonify, request
from ..model import Story, StoryLine, Intent, Action
from . import api
from .. import db


@api.route('/stories', methods=['POST'])
def create_story():
    story = Story(
        story_name=request.json.get('storyName'),
        domain_id=request.json.get('domainId')
    )
    db.session.add(story)
    try:
        db.session.commit()
        return jsonify(story.to_json()), 201
    except Exception as e:
        db.session.rollback()
        return 'Bad request', 400


@api.route('/stories')
def get_stories():
    stories = Story.query.all()
    stories_json = []
    for story in stories:
        stories_json.append(story.to_json())
    return jsonify(stories_json)


@api.route('/stories/<int:story_id>')
def get_story(story_id):
    story = Story.query.get(story_id)
    if story:
        return jsonify(story.to_json())
    else:
        return 'Bad request', 400


@api.route('/stories/<int:story_id>', methods=['PUT'])
def update_story(story_id):
    story = Story.query.get(story_id)
    story.storyName = request.json.get('storyName')
    story.story_lines = []
    for index, storyLine in enumerate(request.json.get('storyLines')):
        story_line = StoryLine(position=index, story_id=story.id)
        story_line.intent = [Intent.query.get(storyLine['intentId'])]
        for actionId in storyLine['actionIds']:
            story_line.actions.append(Action.query.get(actionId))
        story.story_lines.append(story_line)
    db.session.add(story)
    try:
        db.session.commit()
        return jsonify(story.to_json()), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return 'Bad request', 400


@api.route('/domains/<int:domain_id>/stories')
def get_stories_domain(domain_id):
    stories = Story.query.filter_by(domain_id=domain_id).all()
    stories_json = []
    for story in stories:
        stories_json.append(story.to_json())
    return jsonify(stories_json)


@api.route('/stories/<int:story_id>', methods=['DELETE'])
def delete_story(story_id):
    story = Story.query.get(story_id)
    if story:
        db.session.delete(story)
        try:
            db.session.commit()
            return 'success', 204
        except Exception as e:
            return 'Bad request', 400
    else:
        return 'Not Found', 404
