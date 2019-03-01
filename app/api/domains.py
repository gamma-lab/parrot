from flask import jsonify, request, send_file
from flask_login import current_user
import zipfile
from io import BytesIO
from ..model import Domain
from . import api
from .. import db


@api.route('/domains', methods=['POST'])
def create_domain():
    domain = Domain(
        domain_name=request.json.get('domainName'),
        user_id=request.json.get('userId')
    )
    db.session.add(domain)
    try:
        db.session.commit()
        return jsonify(domain.to_json()), 201
    except Exception as e:
        db.session.rollback()
        return 'Bad request', 400


@api.route('/domains')
def get_domains():
    domains = Domain.query.all()
    domains_json = []
    for domain in domains:
        domains_json.append(domain.to_json())
    return jsonify(domains_json)


@api.route('/domains/<int:domain_id>')
def get_domain(domain_id):
    domain = Domain.query.get(domain_id)
    if domain:
        return jsonify(domain.to_json())
    else:
        return 'Bad request', 400


@api.route('/domains/<int:domain_id>', methods=['PUT'])
def update_domain(domain_id):
    domain = Domain.query.get(domain_id)
    if domain:
        domain.domain_name = request.json.get('domainName')
        db.session.add(domain)
        try:
            db.session.commit()
            return jsonify(domain.to_json())
        except Exception as e:
            return 'Bad request', 400
    else:
        return 'Not Found', 404


@api.route('/domains/<int:domain_id>', methods=['DELETE'])
def delete_domain(domain_id):
    domain = Domain.query.get(domain_id)
    if domain:
        if current_user.current_domain_id == domain.id:
            current_user.current_domain_id = None
            db.session.add(current_user)
        db.session.delete(domain)
        try:
            db.session.commit()
            return 'Success', 204
        except Exception as e:
            return 'Bad request', 400
    else:
        return 'Not Found', 404


@api.route('/domains/<int:domain_id>/export')
def export_domain(domain_id):
    domain = Domain.query.get(domain_id)
    if domain:
        domain_json = domain.to_json()
        zip_file = BytesIO()
        nlu_file = ''
        domain_file = ''
        stories_file = ''

        domain_file += 'intents:\n'
        for intent in domain_json['intents']:
            domain_file += ' - {}\n'.format(intent['intentName'])
            nlu_file += '## intent: {}\n'.format(intent['intentName'])
            for sentence in intent['userSays'].split(';'):
                nlu_file += '- {}\n'.format(sentence)
            nlu_file += '\n'

        for story in domain_json['stories']:
            stories_file += '## {}\n'.format(story['storyName'])
            for story_line in story['storyLines']:
                stories_file += '* {}\n'.format(
                    story_line['intent']['intentName'])
                for action in story_line['actions']:
                    stories_file += '  - {}\n'.format(action['actionName'])
            stories_file += '\n'

        actions_str = '\nactions:\n'
        templates_str = '\ntemplates:\n'
        for action in domain_json['actions']:
            actions_str += ' - {}\n'.format(action['actionName'])
            templates_str += '  {}:\n'.format(action['actionName'])
            for agent_response in action['agentResponses'].split(';'):
                templates_str += '    - "{}"\n'.format(agent_response)
        with zipfile.ZipFile(zip_file, 'w') as zf:
            zf.writestr('nlu.md', nlu_file)
            zf.writestr('stories.md', stories_file)
            zf.writestr('domain.yml',
                        domain_file + actions_str + templates_str)
        zip_file.seek(0)
        return send_file(zip_file, attachment_filename='domain.zip',
                         as_attachment=True)
        # return jsonify(domain.to_json())
    else:
        return 'Not Found', 404


@api.route('/domains/<int:domain_id>/current_domain')
def set_current_domain(domain_id):
    domain = Domain.query.get(domain_id)
    if domain:
        current_user.current_domain_id = domain.id
        db.session.add(current_user)
        try:
            db.session.commit()
            return 'Success', 200
        except Exception as e:
            return 'Bad request', 400
    else:
        return 'Not Found', 404
