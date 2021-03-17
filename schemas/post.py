from marshmallow import Schema, fields, validate
from schemas.user import UserSchema
from flask import url_for


class PostSchema(Schema):
    class Meta():
        ordered = True

    id = fields.Integer(dump_only=True)
    value = fields.String(required=True, validate=[validate.Length(max=1000)])
    description = fields.String(validate=[validate.Length(max=100)])
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    author = fields.Nested(UserSchema, attribute='user', dump_only=True, only=['id', 'username'])
    cover_image = fields.Method(serialize='dump_cover_image_url')

    def dump_cover_image_url(self, recipe):
        if recipe.cover_image:
            return url_for('static', filename='images/cover_images/{}'.format(recipe.cover_image), _external=True)
        return None
