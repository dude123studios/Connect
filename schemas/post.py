from marshmallow import Schema, fields, validate
from schemas.user import UserSchema
from flask import url_for


class PostSchema(Schema):
    class Meta():
        ordered = True

    id = fields.Integer(dump_only=True)
    value = fields.String(required=True, validate=[validate.Length(max=2000)])
    description = fields.String(validate=[validate.Length(max=100)])
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    author = fields.Nested(UserSchema, attribute='user', dump_only=True, only=['id', 'username'])
    image = fields.Method(serialize='dump_image_url')
    likes = fields.Integer(dump_only=True)

    def dump_image_url(self, post):
        if post.image:
            return url_for('static', filename='images/cover_images/{}'.format(post.image), _external=True)
        return None
