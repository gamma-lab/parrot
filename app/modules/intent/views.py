import re
from flask import render_template, redirect, url_for, request
from flask_login import current_user
from ...model import Intent, UserSaysExample
from . import intent
from ... import db


@intent.route('/all')
def all_intents():
    """Intents of current domain."""
    intents = current_user.current_domain.intents
    return render_template('intent/intent_all.html',
                           intents=intents)


@intent.route('/<int:intent_id>')
def info_intent(intent_id):
    intent = Intent.query.get_or_404(intent_id)
    return render_template('intent/intent_form.html', action='create')


@intent.route('/add', methods=['GET', 'POST'])
def add_intent():
    if request.method == 'POST':
        intent = Intent(
            intent_name=request.form.get('intent_name'),
            domain_id=current_user.current_domain_id)
        for example_id in request.form.get('examples')[1:-1].split(';'):
            example = UserSaysExample.query.get(example_id)
            if example:
                intent.user_says_examples.append(example)
        if request.form.get('user_says_input'):
            intent.user_says_examples.append(
                UserSaysExample(content=request.form.get('user_says_input')))
        db.session.add(intent)
        try:
            db.session.commit()
            return redirect(url_for('intent.all_intents'))
        except Exception as e:
            # add flash
            db.session.rollback()
    return render_template('intent/intent_form.html', action='create')


@intent.route('/edit/<int:intent_id>', methods=['GET', 'POST'])
def edit_intent(intent_id):
    """Edit intent."""
    intent = Intent.query.get_or_404(intent_id)
    if request.method == 'POST':
        intent.intent_name = request.form.get('intent_name')
        intent.user_says_examples = []
        for example_id in request.form.get('examples')[1:-1].split(';'):
            example = UserSaysExample.query.get(example_id)
            if example:
                intent.user_says_examples.append(example)
        if request.form.get('user_says_input'):
            intent.user_says_examples.append(
                UserSaysExample(content=request.form.get('user_says_input')))
        db.session.add(intent)
        try:
            db.session.commit()
            return redirect(url_for('intent.all_intents'))
        except Exception as e:
            # add flash
            db.session.rollback()
    return render_template('intent/intent_form.html', action='edit',
                           intent=intent)
