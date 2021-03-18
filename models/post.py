from extensions import db
from sqlalchemy import asc, desc, or_


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(1000))
    description = db.Column(db.String(100), default=None)
    created_at = db.Column(db.DateTime(), nullable=False,
                           server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False,
                           server_default=db.func.now(), onupdate=db.func.now())
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    image = db.Column(db.String(100), default=None)
    num_likes = db.Column(db.Integer(), default=0)
    comments = db.relationship('Comment', backref='post')

    @classmethod
    def get_by_id(cls, post_id):
        return cls.query.filter_by(id=post_id).first()

    @classmethod
    def get_all_by_user(cls, page, per_page, user_id):
        return cls.query.filter_by(user_id=user_id). \
            order_by(desc(cls.created_at)).paginate(page=page, per_page=per_page, max_per_page=100)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()