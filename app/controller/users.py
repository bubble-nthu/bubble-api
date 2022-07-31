from flask import jsonify, request, current_app, url_for, abort
from . import api
from ..models import User, Post
from app import db
from app.controller.auth import token_auth
from app.lib.json_request_body import JsonRequestBody

@api.route('/users', methods=['POST'])
def new_user():
    user_info = JsonRequestBody.parse_json_from_request(request)
    user = User(username=user_info["username"], email=user_info["email"], password=user_info["password"])
    db.session.add(user)
    db.session.commit()

    msg = {
        'message': 'Account created',
        'data': user.to_json()
    }

    return jsonify(msg), 201, \
            {'Location': url_for('api.get_user', id=user.id)}


@api.route('/users/<int:id>')
@token_auth.login_required
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/users/<int:id>/posts/')
@token_auth.login_required
def get_user_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['BUBBLE_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_posts', id=id, page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_posts', id=id, page=page+1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/users/<int:id>/timeline/')
@token_auth.login_required
def get_user_followed_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.followed_posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['BUBBLE_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_followed_posts', id=id, page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_followed_posts', id=id, page=page+1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })
