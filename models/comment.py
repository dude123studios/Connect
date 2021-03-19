from extensions import db
from sqlalchemy import asc, desc, or_

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    value = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False,
                           server_default=db.func.now())
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))
    likes = db.Column(db.Integer())
    @classmethod
    def get_all_from_post(cls, post_id, page, per_page):
        return cls.query.filter_by(post_id=post_id).order_by(desc(getattr(cls, '')))

    @classmethod
    def get_users_pending_sent(cls, user_id):
        return cls.query.filter_by(second_id=user_id, pending=False).all()
    def delete(self):
        db.session.remove(self)
        db.session.commit()
    def save(self):
        db.session.add(self)
        db.session.commit()