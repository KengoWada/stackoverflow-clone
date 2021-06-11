from datetime import datetime

from api import db


class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __str__(self):  # pragma: no cover
        return self.body

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
