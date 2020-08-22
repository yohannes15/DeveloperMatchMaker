import os
import secrets
import datetime
import json
from PIL import Image
from flask import url_for, flash, redirect, request, current_app, jsonify
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

@app.route("/api/edit_interests", methods=["PUT"])
@jwt_required
def edit_interests():
    user_id = get_jwt_identity()
    if user_id and request.method == 'PUT':
        data = request.json
        YourFavoriteProgrammingLanguage = data['YourFavoriteProgrammingLanguage']
        SecondFavouriteProgrammingLanguage = data['SecondFavouriteProgrammingLanguage']
        ChooseYourSpecialityDatabaseKnowledge = data['ChooseYourSpecialityDatabaseKnowledge']
        FavoriteDatabaseManagementSystem = data['FavoriteDatabaseManagementSystem']
        YourFieldOfInterest = data['YourFieldOfInterest']
        WhichStatementBelowDescribesYouMostAccurately = data['WhichStatementBelowDescribesYouMostAccurately']
        WhatisYourExperienceLevel = data['WhatisYourExperienceLevel']

        user_interest = Interest.query.filter_by(user_id=user_id).first()

        user_interest.fav_programming_lang_id=YourFavoriteProgrammingLanguage
        user_interest.second_fav_lang_id=SecondFavouriteProgrammingLanguage
        user_interest.database_knowledge_id=ChooseYourSpecialityDatabaseKnowledge
        user_interest.fav_database_system_id=FavoriteDatabaseManagementSystem
        user_interest.field_interest_id=YourFieldOfInterest
        user_interest.programmer_type_id=WhichStatementBelowDescribesYouMostAccurately
        user_interest.experience_id=WhatisYourExperienceLevel

        db.session.commit()

        return jsonify({
            'success': 'Interests edited'
        })
    
    else:
        return jsonify({
            'error': 'Error with user data or user login'
        })


@app.route("/api/edit_profile", methods=["PUT"])
@jwt_required
def edit_profile():
    user_id = get_jwt_identity()
    if user_id and request.method == 'PUT':
        current_user = User.query.filter_by(id=user_id).first()
        if request.files["profilepic"]:
            picture_file = save_picture(request.files["profilepic"])
            print("pic",picture_file)
            current_user.image_file = picture_file
        
        current_user.username = request.form["username"]
        current_user.email = request.form["email"]
        db.session.commit()

        return jsonify({
            'success': "profile edited"
        })
    
    else:
        return jsonify({
            'error': 'error'
        })


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    print(app.root_path)
    picture_path = os.path.join('/Users/yohannes/Developer/DeveloperMatchMaker/frontend/public/', 'assets/images', picture_fn)

    output_size = (568, 528)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn




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


@app.route("/api/get_selected_user/<user>", methods=["GET"])
@jwt_required
def get_selected_user(user):
    user_id = get_jwt_identity()
    if user_id:
        selected_user = User.query.filter_by(username=user).first()
        userid = selected_user.id

        user_interests = Interest.query.filter_by(user_id=userid).first()

        user_fav_programming_lang_id = user_interests.fav_programming_lang_id
        user_second_fav_lang_id = user_interests.second_fav_lang_id
        user_database_knowledge_id = user_interests.database_knowledge_id
        user_fav_database_system_id = user_interests.fav_database_system_id
        user_field_interest_id = user_interests.field_interest_id
        user_programmer_type_id = user_interests.programmer_type_id
        user_experience_id= user_interests.experience_id

        fav_lang = FavProgrammingLang.query.filter_by(fav_lang_id=user_fav_programming_lang_id).first()
        second_fav_lang = SecondFavProgrammingLang.query.filter_by(fav_lang_id=user_second_fav_lang_id).first()
        database_knowledge = DatabaseKnowledge.query.filter_by(database_knowledge_id=user_database_knowledge_id).first()
        fav_database_system = FavDatabaseSystem.query.filter_by(fav_database_system_id=user_fav_database_system_id).first()
        field_interest = FieldInterest.query.filter_by(field_interest_id=user_field_interest_id).first()
        programmer_type = ProgrammerType.query.filter_by(programmer_type_id=user_programmer_type_id).first()
        experience = ExperienceLevel.query.filter_by(experience_id=user_experience_id).first()

        selected_interests = []
        selected_interests.append(fav_lang.fav_lang_name)
        selected_interests.append(second_fav_lang.fav_lang_name)
        selected_interests.append(database_knowledge.database_knowledge_name)
        selected_interests.append(fav_database_system.fav_database_system_name)
        selected_interests.append(field_interest.field_interest_name)
        selected_interests.append(programmer_type.programmer_type_name)
        selected_interests.append(experience.experience_name)

        user_schema = UserSchema()

        selected_user = user_schema.dump(selected_user)

        return jsonify({
            "selected_user": selected_user,
            "current_user": user_id,
            "selected_interests": selected_interests
        })
    else:
        return jsonify({
            'error': 'Could not get user interests'
        })

@app.route("/api/get_account_details", methods=["GET"])
@jwt_required
def get_account_details():
    user_id = get_jwt_identity()
    if user_id:
        current_user = User.query.filter_by(id=user_id).first()
        user_interests = Interest.query.filter_by(user_id=user_id).first()

        user_fav_programming_lang_id = user_interests.fav_programming_lang_id
        user_second_fav_lang_id = user_interests.second_fav_lang_id
        user_database_knowledge_id = user_interests.database_knowledge_id
        user_fav_database_system_id = user_interests.fav_database_system_id
        user_field_interest_id = user_interests.field_interest_id
        user_programmer_type_id = user_interests.programmer_type_id
        user_experience_id= user_interests.experience_id

        fav_lang = FavProgrammingLang.query.filter_by(fav_lang_id=user_fav_programming_lang_id).first()
        second_fav_lang = SecondFavProgrammingLang.query.filter_by(fav_lang_id=user_second_fav_lang_id).first()
        database_knowledge = DatabaseKnowledge.query.filter_by(database_knowledge_id=user_database_knowledge_id).first()
        fav_database_system = FavDatabaseSystem.query.filter_by(fav_database_system_id=user_fav_database_system_id).first()
        field_interest = FieldInterest.query.filter_by(field_interest_id=user_field_interest_id).first()
        programmer_type = ProgrammerType.query.filter_by(programmer_type_id=user_programmer_type_id).first()
        experience = ExperienceLevel.query.filter_by(experience_id=user_experience_id).first()

        selected_interests = []

        selected_interests.append(fav_lang.fav_lang_name)
        selected_interests.append(second_fav_lang.fav_lang_name)
        selected_interests.append(database_knowledge.database_knowledge_name)
        selected_interests.append(fav_database_system.fav_database_system_name)
        selected_interests.append(field_interest.field_interest_name)
        selected_interests.append(programmer_type.programmer_type_name)
        selected_interests.append(experience.experience_name)

        user_schema = UserSchema()
        current_user = user_schema.dump(current_user)

        return jsonify({
            "selected_interests": selected_interests,
            "current_user": current_user
        })
    else:
        return jsonify({
            'error': 'Could not get current user data'
        })

@app.route("/api/send_message/<user>", methods=["POST"])
@jwt_required
def send_message(user):
    user_id = get_jwt_identity()
    if user_id:
        recipient = User.query.filter_by(username=user).first()
        current_user = User.query.filter_by(id=user_id).first()
        
        data = request.json
        message = data['message']     
        msg = Message(sender=current_user, recipient=recipient, body=message)
        db.session.add(msg)
        recipient.add_notification('unread_message_count', recipient.new_messages())
        db.session.commit()

        return jsonify({
            'success': 'sent_message'
        })
    else:
        return jsonify({
            'error': 'trouble sending message'
        })

@app.route("/api/messages", methods=["GET"])
@jwt_required
def messages():
    user_id = get_jwt_identity()
    if user_id:
        current_user = User.query.filter_by(id=user_id).first()
        current_user.last_message_read_time = datetime.datetime.utcnow()
        current_user.add_notification('unread_message_count', 0)
        db.session.commit()
        messages = current_user.messages_received.order_by(
            Message.timestamp.desc()).all()
        
        user_schema = UserSchema(many=True)

        message_schema = MessageSchema(many=True)
        messages = message_schema.dump(messages)

        users_stack = User.query.filter(User.id != user_id)
        users_stack = user_schema.dumps(users_stack)
        users_stack = json.loads(users_stack)

        return jsonify({
            # 'next_url': next_url,
            # 'prev_url': prev_url,
            'messages': messages,
            'users_stack': users_stack
        })
    else:
        return jsonify({
            'error': 'trouble rendering messages'
        })

@app.route("/api/notifications", methods=["GET"])
@jwt_required
def notifications():
    user_id = get_jwt_identity()
    if user_id:
        since = request.args.get('since', 0.0, type=float)
        current_user = User.query.filter_by(id=user_id).first()

        notifications = current_user.notifications.filter(
            Notification.timestamp > since).order_by(Notification.timestamp.asc())
        
        for n in notifications:
            print("hey", n.get_data())
        
        notification_schema = NotificationSchema(many=True)
        notifications = notification_schema.dump(notifications)

        print(notifications)

        new_messages = current_user.new_messages()

        user_schema = UserSchema()
        current_user = user_schema.dump(current_user)
        
        print("since", since)
        
        return jsonify({
            'notifications': notifications,
            'current_user': current_user,
            'new_messages': new_messages,
            'success': True
        })
    else:
        return jsonify({
            'error': "couldn't render notifcations"
        })
        
