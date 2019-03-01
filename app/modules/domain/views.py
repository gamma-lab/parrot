import os
import json
from flask import request, render_template, redirect, url_for
from flask_login import current_user
from ...model import Domain, Intent, Action, Story, StoryLine
from . import domain
from ... import db


@domain.route('/add', methods=['GET', 'POST'])
def add_domain():
    """Create new domain."""
    if request.method == 'POST':
        domain = Domain(domain_name=request.form.get('domain_name'),
                        language=request.form.get('language'),
                        description=request.form.get('description'),
                        user_id=current_user.id)
        db.session.add(domain)
        current_user.current_domain = domain
        db.session.add(current_user)
        try:
            db.session.commit()
            return redirect(url_for('domain.info_domain', domain_id=domain.id))
        except Exception as e:
            # add flash
            db.session.rollback()
    return render_template('domain/domain_form.html', action='create')


@domain.route('/add_default_domain')
def add_default_domain():
    """Create default domain."""
    # already exists
    domain = Domain.query.filter_by(
        domain_name='Default', user_id=current_user.id).first()
    if domain:
        return redirect(
            url_for(
                'domain.info_domain',
                domain_id=domain.id))
    domain = Domain(domain_name='Default',
                    language='English',
                    description='This domain includes the files for Rasa Get Started tutorial at: https://rasa.com/docs/get_started_step1/',
                    user_id=current_user.id)
    db.session.add(domain)
    current_user.current_domain = domain
    db.session.add(current_user)

    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__ + '/../../')),
                     'static',
                     'data',
                     'default_domain.json')) as f:
        data = json.load(f)
        for _intent in data['intents']:
            intent = Intent(intent_name=_intent['intent_name'],
                            user_says=';'.join(_intent['user_says']))
            domain.intents.append(intent)
        for _action in data['actions']:
            action = Action(
                action_name=_action['action_name'],
                agent_responses=';'.join(_action['agent_responses']))
            domain.actions.append(action)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return redirect(url_for('domain.all_domains'))
        for _story in data['stories']:
            story = Story(story_name=_story['story_name'], domain_id=domain.id)
            for index, _story_line in enumerate(_story['story_lines']):
                story_line = StoryLine(position=index)
                story_line.intent = [
                    Intent.query.filter_by(
                        intent_name=_story_line['intent_name'],
                        domain_id=domain.id).first()]
                for __action in _story_line['action_names']:
                    story_line.actions.append(
                        Action.query.filter_by(
                            action_name=__action, domain_id=domain.id).first())
                story.story_lines.append(story_line)
            db.session.add(story)
    try:
        db.session.commit()
        return redirect(url_for('domain.info_domain', domain_id=domain.id))
    except Exception as e:
        # add flash
        db.session.rollback()
        return redirect(url_for('domain.all_domains'))


@domain.route('/all', methods=['GET'])
def all_domains():
    """All domains."""
    domains = Domain.query.all()
    return render_template('domain/domain_all.html',
                           domains=domains)


@domain.route('/<int:domain_id>', methods=['GET'])
def info_domain(domain_id):
    """Info of then domain."""
    domain = Domain.query.get_or_404(domain_id)
    return render_template('domain/domain_info.html',
                           domain=domain)


@domain.route('/edit/<int:domain_id>', methods=['GET', 'POST'])
def edit_domain(domain_id):
    """Edit domain."""
    domain = Domain.query.get_or_404(domain_id)
    if request.method == 'POST':
        domain.domain_name = request.form.get('domain_name')
        domain.language = request.form.get('language')
        domain.description = request.form.get('description')
        db.session.add(domain)
        try:
            db.session.commit()
            return redirect(url_for('domain.all_domains'))
        except Exception as e:
            # add flash
            db.session.rollback()
    return render_template('domain/domain_form.html', action='edit',
                           domain=domain)
