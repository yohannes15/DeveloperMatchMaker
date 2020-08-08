import os
import secrets
import datetime
# from PIL import Image
from flask import render_template, url_for, flash, redirect, request, current_app, jsonify
from matcher import app, db, bcrypt
# from matcher.forms import RegistrationForm, LoginForm, EditProfileForm, MessageForm
from matcher.models import *
from flask_login import login_user, current_user, logout_user, login_required
# from matcher.queries import *
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
    
    

