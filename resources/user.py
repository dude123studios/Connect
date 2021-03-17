from flask import request, url_for, render_template
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required
from models.user import User
from schemas.user import UserSchema
from webargs import fields
from webargs.flaskparser import use_kwargs
from schemas.post import PostSchema
from schemas.pagination import PostPaginationSchema
from models.post import Post
from models.friend import Friend
from utils import verify_token, generate_token, save_image, clear_cache
from utils import Mail
import os
from extensions import image_set, limiter

user_schema = UserSchema()
user_avatar_schema = UserSchema(only=('avatar_url',))
user_public_schema = UserSchema(exclude=('email',))
recipe_pagination_schema= PostPaginationSchema()
mailgun = Mail(domain=os.environ.get('MAILGUN_DOMAIN'),
                  api_key=os.environ.get('MAILGUN_API_KEY'))


class UserListResource(Resource):
    def post(self):
        json_data = request.get_json()

        data, errors = user_schema.load(data=json_data)
        if errors:
            return {'message':'Validation errors', 'errors':errors}, HTTPStatus.BAD_REQUEST
        if User.get_by_username(data.get('username')):
            return {'message': 'username already taken'}, HTTPStatus.BAD_REQUEST
        if User.get_by_email(data.get('email')):
            return {'message': 'email already taken'}, HTTPStatus.BAD_REQUEST

        user = User(**data)
        user.save()
        token = generate_token(user.email, salt='activate')
        subject = 'Please confirm your registration.'
        link = url_for('useractivateresource', token = token,_external=True)
        text = 'Hi, thanks for using Connect!'
        mailgun.send_email(to=user.email, subject=subject, text=text,
                           html=render_template('activation.html', link=link))
        return user_schema.dump(user).data, HTTPStatus.CREATED

class UserAvatarUploadResource(Resource):
    @jwt_required
    def put(self):
        file = request.files.get('avatar')
        if not file:
            return {'message':'Not a valid image'}, HTTPStatus.BAD_REQUEST
        if not image_set.file_allowed(file,file.filename):
            return {'message':'File type not supported'}, HTTPStatus.BAD_REQUEST
        user = User.get_by_id(id=get_jwt_identity())
        if user.avatar_image:
            avatar_path = image_set.path(filename=user.avatar_image, folder='avatars')
            if os.path.exists(avatar_path):
                os.remove(avatar_path)
        filename = save_image(file, 'avatars')
        user.avatar_image = filename
        user.save()
        clear_cache('/recipes')
        return user_avatar_schema.dump(user).data, HTTPStatus.OK
class UserActivateResource(Resource):
    def get(self,token):
        email = verify_token(token=token, salt='activate')
        if email is False:
            return {'message':'Invalid token or token expired'}, HTTPStatus.BAD_REQUEST
        user = User.get_by_email(email)
        if not user:
            return {'message':'User not found'}, HTTPStatus.NOT_FOUND
        if user.is_active is True:
            return {'message':'The user account is already activated'}, HTTPStatus.BAD_REQUEST
        user.is_active=True
        user.save()
        return {}, HTTPStatus.NO_CONTENT

class UserPostListResource(Resource):
    decorators = [limiter.limit('3/minute;30/hour;300/day', methods=['GET'], error_message='Too many requests')]
    @jwt_optional
    @use_kwargs({
                 'page':fields.Int(missing=1),'per_page':fields.Int(missing=20)})
    def get(self,page,per_page,username):
        user = User.get_by_username(username)
        if user is None:
            return {'message':'User not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        if user.id == current_user:
            pass
        recipes = Post.get_all_by_user(user_id=user.id, page=page,per_page=per_page)

        return recipe_pagination_schema.dump(recipes).data, HTTPStatus.OK


class UserResource(Resource):

    @jwt_optional
    def get(self, username):

        user = User.get_by_username(username)
        if user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if current_user == user.id:
            data = user_schema.dump(user).data
        else:
            data = user_public_schema.dump(user).data
        return data, HTTPStatus.OK

class UserFriendResource(Resource):

    @jwt_required
    def post(self, username):
        user = User.get_by_username(username)
        if user is None:
            return {'message':'user not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()

    @jwt_required
    def put(self, username):
        user = User.get_by_username(username)
        if user is None:
            return {'message':'user not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()



class MeResource(Resource):
    @jwt_required
    def get(self):
        user = User.get_by_id(id=get_jwt_identity())
        return user_schema.dump(user).data, HTTPStatus.OK

    @jwt_required
    def put(self):
        user = User.get_by_id(id=get_jwt_identity())
        json_data = request.get_json()
        data, errors = user_schema.load(data=json_data)
        if errors:
            return {'message':'Validation errors', 'errors':errors}, HTTPStatus.BAD_REQUEST
        user = User(**data)
        user.save()
        return user_schema.dump(user).data, HTTPStatus.CREATED