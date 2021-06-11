from datetime import datetime

from api import db
from werkzeug.security import check_password_hash, generate_password_hash


answer_likes = db.Table(
    'answer_likes',
    db.Column('user_id', db.ForeignKey('users.id')),
    db.Column('answer_id', db.ForeignKey('answers.id'))
)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(256))
    questions = db.relationship('Question', backref='author', lazy='dynamic')
    answers = db.relationship('Answer', backref='author', lazy='dynamic')
    liked_answers = db.relationship(
        'Answer', secondary=answer_likes, backref='liked_by', lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __str__(self):  # pragma: no cover
        return self.username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def like_answer(self, answer):
        self.liked_answers.append(answer)
        db.session.commit()

    def dislike_answer(self, answer):
        self.liked_answers.remove(answer)
        db.session.commit()

    def has_liked_answer(self, answer):
        return self.liked_answers.filter(answer_likes.c.answer_id == answer.id).count() > 0

    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        return data
