from extensions import db
from sqlalchemy import asc, desc, or_, and_

class Dm(db.Model):
    __tablename__ = 'dm'
    id = db.Column(db.Integer, primary_key = True)
    sent_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    received_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    value = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False,
                           server_default=db.func.now())

    @classmethod
    def get_all_by_pair(cls, x, y):
        return cls.query.filter(
            or_(and_(cls.sent_id.is_(x), cls.received_id.is_(y)),
                and_(cls.sent_id.is_(y), cls.received_id.is_(x)))
        ).order_by(asc(getattr(cls, 'created_at')))
    def delete(self):
        db.session.remove(self)
        db.session.commit()
    def save(self):
        db.session.add(self)
        db.session.commit()