from api import db
from datetime import datetime


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

    def update(self, data):
        for field in ['title', 'body']:
            if field in data:
                setattr(self, field, data[field])

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
