from sqlalchemy import (
    ForeignKey, Integer, String, DateTime, Text)
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from . import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(Integer, primary_key=True, index=True)
    first_name = db.Column(String(64))
    last_name = db.Column(String(64))
    full_name = db.column_property(first_name + ' ' + last_name)
    email = db.Column(Text, unique=True, index=True)
    password_hash = db.Column(String(128))
    member_since = db.Column(DateTime, default=datetime.utcnow)
    current_domain_id = db.Column(Integer, ForeignKey('domains.id'))
    current_domain = db.relationship(
        'Domain',
        backref=db.backref('current_user', uselist=False),
        foreign_keys='User.current_domain_id')
    domains = db.relationship('Domain', backref='creator', lazy=True,
                              foreign_keys='Domain.user_id')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: %r, name: %r>' \
            % (self.id, self.full_name)

    def to_json(self):
        domains = [domain.to_json() for domain in self.domains]
        return {
            'userId': self.id,
            'name': self.full_name,
            'email': self.email,
            'memberSince': str(self.member_since),
            'domains': domains
        }


class Domain(db.Model):
    __tablename__ = 'domains'

    id = db.Column(Integer, primary_key=True, index=True)
    domain_name = db.Column(String(64), nullable=False)
    language = db.Column(String(16), nullable=False)
    description = db.Column(Text, default='')
    created_timestamp = db.Column(DateTime, default=datetime.utcnow)
    updated_timestamp = db.Column(DateTime, default=datetime.utcnow)
    user_id = db.Column(Integer, ForeignKey('users.id'), nullable=False)
    stories = db.relationship('Story', backref='domain', lazy=True,
                              cascade='all, delete-orphan')
    intents = db.relationship('Intent', backref='domain', lazy=True,
                              cascade='all, delete-orphan')
    actions = db.relationship('Action', backref='domain', lazy=True,
                              cascade='all, delete-orphan')

    def __repr__(self):
        return '<Domain: %r, domain_name: %r>' \
            % (self.id, self.domain_name)

    def to_json(self):
        stories = [story.to_json() for story in self.stories]
        intents = [intent.to_json() for intent in self.intents]
        actions = [action.to_json() for action in self.actions]
        return {
            'domainId': self.id,
            'language': self.language,
            'domainName': self.domain_name,
            'userId': self.user_id,
            'stories': stories,
            'intents': intents,
            'actions': actions
        }


story_line_intent = db.Table('story_line_intent',
                             db.Column('story_line_id', Integer,
                                       ForeignKey('story_lines.id'),
                                       primary_key=True),
                             db.Column('intent_id', Integer,
                                       ForeignKey('intents.id'),
                                       primary_key=True)
                             )

story_line_action = db.Table('story_line_action',
                             db.Column('story_line_id', Integer,
                                       ForeignKey('story_lines.id'),
                                       primary_key=True),
                             db.Column('action_id', Integer,
                                       ForeignKey('actions.id'),
                                       primary_key=True)
                             )


class Story(db.Model):
    __tablename__ = 'stories'

    id = db.Column(Integer, primary_key=True, index=True)
    story_name = db.Column(String(64), nullable=False)
    created_timestamp = db.Column(DateTime, default=datetime.utcnow)
    updated_timestamp = db.Column(DateTime, default=datetime.utcnow)
    domain_id = db.Column(Integer, ForeignKey('domains.id'), nullable=False)
    story_lines = db.relationship('StoryLine', backref='story', lazy='dynamic',
                                  cascade='all, delete-orphan')

    def __repr__(self):
        return '<Story: %r, story_name: %r>' \
            % (self.id, self.story_name)

    def to_json(self):
        story_lines = [
            story_line.to_json() for story_line in self.story_lines.order_by(
                StoryLine.position.asc())]
        return {
            'storyId': self.id,
            'storyName': self.story_name,
            'domainId': self.domain_id,
            'storyLines': story_lines
        }

    @property
    def actions(self):
        return set([
            story_line for story_line in self.story_lines for
            action in story_line.actions])

    @property
    def intents(self):
        return set([
            story_line for story_line in self.story_lines for
            intent in story_line.intent])


class Intent(db.Model):
    __tablename__ = 'intents'

    id = db.Column(Integer, primary_key=True, index=True)
    intent_name = db.Column(String(64), nullable=False)
    created_timestamp = db.Column(DateTime, default=datetime.utcnow)
    updated_timestamp = db.Column(DateTime, default=datetime.utcnow)
    user_says_examples = db.relationship('UserSaysExample', backref='intent',
                                         lazy=True,
                                         cascade='all, delete-orphan')
    domain_id = db.Column(Integer, ForeignKey('domains.id'), nullable=False)

    def __repr__(self):
        return '<Intent: %r, intent_name: %r>' \
            % (self.id, self.intent_name)

    def to_json(self):
        user_says_examples = [
            user_says_example.to_json() for
            user_says_example in self.user_says_examples
        ]
        return {
            'intentId': self.id,
            'intentName': self.intent_name,
            'domainId': self.domain_id,
            'user_says_examples': user_says_examples
        }


class UserSaysExample(db.Model):
    __tablename__ = 'user_says_examples'

    id = db.Column(Integer, primary_key=True, index=True)
    content = db.Column(Text, default='')
    intent_id = db.Column(Integer, ForeignKey('intents.id'))
    entities = db.relationship('UserSaysExampleEntityAssociation',
                               back_populates='user_says_example',
                               lazy=True, cascade='all, delete-orphan')


class Entity(db.Model):
    __tablename__ = 'entities'

    id = db.Column(Integer, primary_key=True, index=True)
    entity_name = db.Column(String(64), nullable=False)
    domain_id = db.Column(Integer, ForeignKey('domains.id'), nullable=False)
    user_says_examples = db.relationship('UserSaysExampleEntityAssociation',
                                         back_populates='entity',
                                         lazy=True,
                                         cascade='all, delete-orphan')


class UserSaysExampleEntityAssociation(db.Model):
    __tablename__ = 'user_says_examples_entities_association'

    id = db.Column(Integer, primary_key=True, index=True)
    value = db.Column(Text, default='')
    start_index = db.Column(Integer)
    end_index = db.Column(Integer)
    entity_id = db.Column(Integer, ForeignKey('entities.id'))
    user_says_example_id = db.Column(Integer,
                                     ForeignKey('user_says_examples.id'))
    entity = db.relationship('Entity', back_populates='user_says_examples')
    user_says_example = db.relationship('UserSaysExample',
                                        back_populates='entities')


class Action(db.Model):
    __tablename__ = 'actions'

    id = db.Column(Integer, primary_key=True, index=True)
    action_name = db.Column(String(64), nullable=False)
    agent_responses = db.Column(Text, default='')
    created_timestamp = db.Column(DateTime, default=datetime.utcnow)
    updated_timestamp = db.Column(DateTime, default=datetime.utcnow)
    domain_id = db.Column(Integer, ForeignKey('domains.id'), nullable=False)

    def __repr__(self):
        return '<Action: %r, action_name: %r>' \
            % (self.id, self.action_name)

    def to_json(self):
        return {
            'actionId': self.id,
            'actionName': self.action_name,
            'domainId': self.domain_id,
            'agentResponses': self.agent_responses
        }


class StoryLine(db.Model):
    __tablename__ = 'story_lines'

    id = db.Column(Integer, primary_key=True, index=True)
    position = db.Column(Integer, nullable=False)
    story_id = db.Column(Integer, ForeignKey('stories.id'), nullable=True)
    # should only have one intent
    intent = db.relationship('Intent', secondary=story_line_intent,
                             lazy='subquery',
                             backref=db.backref('story_line', lazy=True))
    actions = db.relationship('Action', secondary=story_line_action,
                              lazy='subquery',
                              backref=db.backref('story_line', lazy=True))

    def __repr__(self):
        return '<StoryLine: %r, story_id: %r>' \
            % (self.id, self.story_id)

    def to_json(self):
        actions_json = []
        for action in self.actions:
            actions_json.append(action.to_json())
        return {
            'intent': self.intent[0].to_json(),
            'actions': actions_json,
            'storyLineId': self.id,
            'storyId': self.story_id,
            'position': self.position
        }
