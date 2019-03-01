from flask import render_template, redirect, url_for, request
from flask_login import current_user
from ...model import Action
from . import action
from ... import db


@action.route('/all')
def all_actions():
    """Actions of current domain."""
    actions = current_user.current_domain.actions
    return render_template('action/action_all.html',
                           actions=actions)


@action.route('/<int:action_id>')
def info_action(action_id):
    action = Action.query.get_or_404(action_id)
    return render_template('main/get_started.html')


@action.route('/add', methods=['GET', 'POST'])
def add_action():
    if request.method == 'POST':
        action = Action(action_name=request.form.get('action_name'),
                        agent_responses=request.form.get('agent_responses'),
                        domain_id=current_user.current_domain_id)
        db.session.add(action)
        try:
            db.session.commit()
            return redirect(url_for('action.all_actions'))
        except Exception as e:
            # add flash
            db.session.rollback()
    return render_template('action/action_form.html', action='create')


@action.route('/edit/<int:action_id>', methods=['GET', 'POST'])
def edit_action(action_id):
    """Edit action."""
    _action = Action.query.get_or_404(action_id)
    if request.method == 'POST':
        _action.action_name = request.form.get('action_name')
        _action.agent_responses = request.form.get('agent_responses')
        db.session.add(_action)
        try:
            db.session.commit()
            return redirect(url_for('action.all_actions'))
        except Exception as e:
            # add flash
            db.session.rollback()
    return render_template('action/action_form.html', action='edit',
                           _action=_action)
