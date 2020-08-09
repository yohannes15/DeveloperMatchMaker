import os
import secrets
import datetime
# from PIL import Image
from flask import render_template, url_for, flash, redirect, request, current_app, jsonify
from matcher import app, db, bcrypt
# from matcher.forms import RegistrationForm, LoginForm, EditProfileForm, MessageForm
from matcher.models import *
from flask_login import login_user, current_user, logout_user, login_required
from matcher.queries import *
from flask_babel import lazy_gettext as _l
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


@app.route("/api/login",  methods=["GET", "POST"])
def login():
    data = request.json
    email = data['email']
    password = data['password']
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        token = create_access_token(identity=user.id)
        return jsonify({'token': token})
    else:
        return jsonify({"error": "Login unsucessful try other email and password"})


@app.route("/api/register", methods=["GET", "POST"])
def register():
    data = request.json
    firstname = data['firstname']
    lastname = data['lastname']
    username = data['username']
    email = data['email']
    password = data['password']
    dateofbirth = data['dateofbirth']
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email=email, password=hashed_password,
                firstname=firstname, lastname=lastname, date_of_birth=dateofbirth)
    db.session.add(user)
    db.session.commit()

    return jsonify({'User': 'Registered'})

@app.route("/api/hasinterests", methods=["GET"])
def has_interests():
    user_id = get_jwt_identity()
    exists = db.session.query(db.exists().where(Interest.interest_id == user_id)).scalar()
    if not exists:
        return jsonify({'error': 'user has not interests'})
    else:
        return jsonify({"success": "user has interests already"})

##USER SPECIFIC

@app.route("/api/users_stack_with_interests")
def users_stack():
    user_id = get_jwt_identity()
    if user_id:
        user_schema = UserSchema(many=True)
        interest_schema = InterestSchema(many=True)

        users_stack = User.query.filter(User.id != user_id)
        users_stack = user_schema.dumps(users_stack)

        interests = Interest.query.all()
        interests = interest_schema.dumps(interests)

        all_interests = [all_fav_programming_lang()[1], all_fav_database_systems()[1], all_field_interests()[1] ,all_experience_level()[1], all_second_fav_lang()[1]] 
        return jsonify({
            'users_stack': users_stack,
            'interests': interests,
            'all_interests': all_interests
        })
    
    else:
        return jsonify({'error': 'Not logged in'})

    




    
    

