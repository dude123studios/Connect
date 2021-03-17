from extensions import db
from sqlalchemy import asc, desc, or_

class Friend(db.Model):
    __tablename__ = 'friend'
    id = db.Column(db.Integer, primary_key = True)
    first_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    second_id = db.Cloumn(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False,
                           server_default=db.func.now(), onupdate=db.func.now())

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_users_friend(cls, user_id):
        return cls.query.filter_by(first_id=user_id).extend(cls.query.filter_by(second_id=user_id))

    def delete(self):
        db.session.remove(self)
        db.session.commit()
    def save(self):
        db.session.add(self)
        db.session.commit()