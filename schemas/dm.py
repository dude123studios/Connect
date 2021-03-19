from marshmallow import Schema, fields, validate
from schemas.user import UserSchema


class DmSchema(Schema):
    class Meta():
        ordered = True

    id = fields.Integer(dump_only=True)
    value = fields.String(required=True, validate=[validate.Length(max=1000)])
    created_at = fields.DateTime(dump_only=True)
    author = fields.Nested(UserSchema, attribute='user', dump_only=True, only=['id', 'username'])
    read = fields.Boolean(dump_only=True)

