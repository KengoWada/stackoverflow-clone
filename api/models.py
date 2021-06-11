from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from . import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128))
    reset_password_token = db.Column(db.String(120), default='')
    questions = db.relationship('Question', backref='author', lazy='dynamic')
    answers = db.relationship('Answer', backref='author', lazy='dynamic')
    liked_answers = db.relationship(
        'AnswerLike', foreign_keys='AnswerLike.user_id', backref='user', lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __str__(self):  # pragma: no cover
        return self.username

    def __repr__(self):  # pragma: no cover
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def like_answer(self, answer):
        like = AnswerLike(user_id=self.id, answer_id=answer.id)
        db.session.add(like)
        db.session.commit()

    def dislike_answer(self, answer):
        AnswerLike.query.filter_by(
            user_id=self.id,
            answer_id=answer.id).delete()
        db.session.commit()

    def has_liked_answer(self, answer):
        return AnswerLike.query.filter(
            AnswerLike.user_id == self.id,
            AnswerLike.answer_id == answer.id).count() > 0

    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        return data


class AnswerLike(db.Model):
    __tablename__ = 'answer_likes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answers.id'))


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    answers = db.relationship('Answer', backref='question', lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __str__(self):  # pragma: no cover
        return self.title

    def __repr__(self):  # pragma: no cover
        return f'<Question {self.title}>'

    def update(self, data):
        for field in ['title', 'body']:
            if field in data:
                setattr(self, field, data[field])

    def get_answer(self, answer_id):
        for answer in self.answers:
            if answer.id == int(answer_id):
                return answer

        return None

    def to_dict(self):
        data = {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'created_at': self.created_at,
            'author': self.author.username,
            'num_answers': self.answers.count(),
            'answers': [answer.to_dict(simple=True) for answer in self.answers]
        }
        return data


class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    likes = db.relationship('AnswerLike', backref='answer', lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __str__(self):  # pragma: no cover
        return self.body

    def __repr__(self):  # pragma: no cover
        return f'<Answer {self.body}>'

    def to_dict(self, simple=False):
        data = {
            'id': self.id,
            'body': self.body,
            'author': self.author.username,
            'likes': self.likes.count()
        }

        if not simple:
            data['question'] = {
                'id': self.question.id, 'title': self.question.title, 'author': self.question.author.username}
            data['author'] = {'id': self.author.id,
                              'username': self.author.username}

        return data
