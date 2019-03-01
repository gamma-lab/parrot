from flask import render_template, redirect, url_for, request
from flask_login import current_user
import re
from ...model import Story, StoryLine, Intent, Action
from . import story
from ... import db


@story.route('/all')
def all_stories():
    """stories of current domain."""
    stories = current_user.current_domain.stories
    return render_template('story/story_all.html',
                           stories=stories)


# @story.route('/<int:story_id>')
# def info_story(story_id):
#     story = Story.query.get_or_404(story_id)
#     return render_template('story/story_form.html', action='create')


@story.route('/add', methods=['GET', 'POST'])
def add_story():
    intents = current_user.current_domain.intents
    actions = current_user.current_domain.actions
    if request.method == 'POST':
        story = Story(story_name=request.form.get('story_name'),
                      domain_id=current_user.current_domain_id)
        db.session.add(story)

        intent_index = 0
        story_line = None
        for item in request.form.get('story_list').split(';'):
            if item.startswith('intent'):
                intent_id = re.search(r'intent-(\d+)', item).group(1)
                story_line = StoryLine(
                    position=intent_index)
                story.story_lines.append(story_line)
                story_line.intent = [
                    Intent.query.get(intent_id)]
                intent_index += 1
            elif item.startswith('action'):
                action_id = re.search(r'action-(\d+)', item).group(1)
                story_line.actions.append(Action.query.get(action_id))
            else:
                pass
        # db.session.add(story)
        try:
            db.session.commit()
            return redirect(url_for('story.all_stories'))
        except Exception as e:
            # add flash
            print(e)
            db.session.rollback()
    return render_template('story/story_form.html', action='create',
                           intents=intents, actions=actions)


@story.route('/edit/<int:story_id>', methods=['GET', 'POST'])
def edit_story(story_id):
    """Edit story."""
    story = Story.query.get_or_404(story_id)
    intents = current_user.current_domain.intents
    actions = current_user.current_domain.actions
    if request.method == 'POST':
        story.story_name = request.form.get('story_name')
        story.story_lines = []
        db.session.add(story)

        intent_index = 0
        story_line = None
        for item in request.form.get('story_list').split(';'):
            if item.startswith('intent'):
                intent_id = re.search(r'intent-(\d+)', item).group(1)
                story_line = StoryLine(
                    position=intent_index)
                story_line.intent = [
                    Intent.query.get(intent_id)]
                story.story_lines.append(story_line)
                intent_index += 1
            elif item.startswith('action'):
                action_id = re.search(r'action-(\d+)', item).group(1)
                story_line.actions.append(Action.query.get(action_id))
            else:
                pass
        try:
            db.session.commit()
            return redirect(url_for('story.all_stories'))
        except Exception as e:
            # add flash
            db.session.rollback()
    return render_template('story/story_form.html', action='edit',
                           story=story, intents=intents, actions=actions)
