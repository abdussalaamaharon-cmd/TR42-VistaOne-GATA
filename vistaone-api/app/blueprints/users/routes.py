from . import users_bp
from flask import request, jsonify
from app.models import db, User
from .schemas import login_schema, user_schema
from app.utils.util import encode_token
from marshmallow import ValidationError

@users_bp.route("/register", methods=['POST'])
def register():
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Check if email already exists
    existing_user = db.session.execute(
        db.select(User).where(User.email == user_data['email'])
    ).scalar_one_or_none()

    if existing_user:
        return jsonify({'message': 'Email already registered', 'status': 'error'}), 400

    # Create new user
    new_user = User(
        name=user_data['name'],
        email=user_data['email'],
        phone=user_data.get('phone')
    )
    new_user.set_password(user_data['password'])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'message': 'User registered successfully',
        'status': 'success'
    }), 201

@users_bp.route("/login", methods=['POST'])
def login():
    try:
        credentials = login_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Find user by email
    user = db.session.execute(
        db.select(User).where(User.email == credentials['email'])
    ).scalar_one_or_none()

    # Check user exists and password is correct
    if not user or not user.check_password(credentials['password']):
        return jsonify({'message': 'Invalid email or password', 'status': 'error'}), 401

    # Generate token
    token = encode_token(user.id)

    return jsonify({
        'message': 'Successfully Logged In',
        'status': 'success',
        'token': token
    }), 200