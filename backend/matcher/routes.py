import os
import secrets
import datetime
import json
# from PIL import Image
from flask import render_template, url_for, flash, redirect, request, current_app, jsonify
from matcher import app, db, bcrypt, jwt
# from matcher.forms import RegistrationForm, LoginForm, EditProfileForm, MessageForm
from matcher.models import *
from flask_login import login_user, current_user, logout_user, login_required
from matcher.queries import *
from flask_babel import lazy_gettext as _l
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, \
    jwt_refresh_token_required, create_refresh_token, get_raw_jwt

@app.route("/api/login",  methods=["GET", "POST"])
def login():
    data = request.json
    email = data['email']
    password = data['password']
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify({'token': token, 'refreshToken': refresh_token})
    else:
        return jsonify({"error": "Login unsucessful try other email and password"})


@app.route("/api/register", methods=["GET", "POST"])
def register():
    data = request.json
    firstname = data['firstname']
    lastname = data['lastname']
    username = data['username']
    email = data['email']
    email.lower()
    password = data['password']
    dateofbirth = data['dateofbirth']
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email=email, password=hashed_password,
                firstname=firstname, lastname=lastname, date_of_birth=dateofbirth)
    db.session.add(user)
    db.session.commit()

    return jsonify({'User': 'Registered'})

@jwt.token_in_blacklist_loader
def check_if_blacklisted_token(decrypted):
    jti = decrypted["jti"]
    return InvalidToken.is_invalid(jti)

@app.route("/api/checkiftokenexpire", methods=["POST"])
@jwt_required
def check_if_token_expire():
    return jsonify({"success": True})

@app.route("/api/refreshtoken", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    identity = get_jwt_identity()
    token = create_access_token(identity=identity)
    return jsonify({"token": token})


@app.route("/api/logout/access", methods=["POST"])
@jwt_required
def access_logout():
    jti = get_raw_jwt()["jti"]
    try:
        invalid_token = InvalidToken(jti=jti)
        invalid_token.save()
        return jsonify({"success": True})
    except Exception as e:
        print(e)
        return {"error": e}


@app.route("/api/logout/refresh", methods=["POST"])
@jwt_required
def refresh_logout():
    jti = get_raw_jwt()["jti"]
    try:
        invalid_token = InvalidToken(jti=jti)
        invalid_token.save()
        return jsonify({"success": True})
    except Exception as e:
        print(e)
        return {"error": e}

@app.route("/api/hasinterests", methods=["GET"])
@jwt_required
def has_interests():
    user_id = get_jwt_identity()
    print(get_jwt_identity())
    exists = db.session.query(db.exists().where(Interest.user_id == user_id)).scalar()
    print('EXISTS', exists)
    if not exists:
        return jsonify({'error': 'user has not interests'})
    else:
        return jsonify({"success": "user has interests already"})

##USER SPECIFIC ############
############################


@app.route("/api/get_interests",  methods=["GET"])
@jwt_required
def users_stack():
    user_id = get_jwt_identity()
    print("bruv", user_id)
    if user_id:
        fav_prog_langs = all_fav_programming_lang()
        second_fav_langs = all_second_fav_lang()
        database_knowledge = all_database_knowledge()
        fav_db_systems = all_fav_database_systems()
        field_interests = all_field_interests()
        programmer_types = all_programmer_types()
        experience_levels = all_experience_level()
        

        all_interests = [fav_prog_langs, second_fav_langs, database_knowledge, fav_db_systems, field_interests, programmer_types, experience_levels]
        print(all_interests)

        return {
            'all_interests': all_interests
        }
    
    else:
        return jsonify({'error': 'Not logged in'})


@app.route("/api/add_interests", methods=["POST"])
@jwt_required
def add_interest():
    user_id = get_jwt_identity()
    if user_id and request.method == 'POST':
            data = request.json
            YourFavoriteProgrammingLanguage = data['YourFavoriteProgrammingLanguage']
            SecondFavouriteProgrammingLanguage = data['SecondFavouriteProgrammingLanguage']
            ChooseYourSpecialityDatabaseKnowledge = data['ChooseYourSpecialityDatabaseKnowledge']
            FavoriteDatabaseManagementSystem = data['FavoriteDatabaseManagementSystem']
            YourFieldOfInterest = data['YourFieldOfInterest']
            WhichStatementBelowDescribesYouMostAccurately = data['WhichStatementBelowDescribesYouMostAccurately']
            WhatisYourExperienceLevel = data['WhatisYourExperienceLevel']

            interest = Interest(
                user_id=user_id,
                fav_programming_lang_id=YourFavoriteProgrammingLanguage,
                second_fav_lang_id=SecondFavouriteProgrammingLanguage,
                database_knowledge_id=ChooseYourSpecialityDatabaseKnowledge,
                fav_database_system_id=FavoriteDatabaseManagementSystem,
                field_interest_id=YourFieldOfInterest,
                programmer_type_id=WhichStatementBelowDescribesYouMostAccurately,
                experience_id=WhatisYourExperienceLevel
            )
            db.session.add(interest)
            db.session.commit()

            return jsonify({
                'interestAdded': "true"
            })
    else:
        return jsonify({
            'error': "ERROR"
        })


@app.route("/api/get_users", methods=["GET"])
@jwt_required
def get_users():
    user_id = get_jwt_identity()
    if user_id:
        user_schema = UserSchema(many=True)
        interest_schema = InterestSchema(many=True)

        users_stack = User.query.filter(User.id != user_id)
        users_stack = user_schema.dumps(users_stack)
        users_stack = json.loads(users_stack)

        interests = Interest.query.all()
        interests = interest_schema.dumps(interests)
        interests = json.loads(interests)

        all_interests = [all_fav_programming_lang(), all_second_fav_lang(), all_fav_database_systems(), all_field_interests(), all_experience_level()]

        return {
            'all_interests': all_interests,
            'users_stack': users_stack,
            'interests': interests
        }

    else:
        return jsonify({
            'error': 'ERROR'
        })


