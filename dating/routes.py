import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, current_app, jsonify
from dating import app, db, bcrypt
from dating.forms import RegistrationForm, LoginForm, EditProfileForm, MessageForm
from dating.models import *
from flask_login import login_user, current_user, logout_user, login_required
from dating.queries import *
import datetime
from flask_babel import lazy_gettext as _l



@app.route("/", methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/home")
@login_required
def home():
    session['user_id'] = current_user.id
    interests = Interest.query.all()
    users_stack = User.query.filter(User.id != current_user.id)
    all_interests = [all_fav_programming_lang()[1], all_fav_database_systems()[1], all_field_interests()[1] ,all_experience_level()[1], all_second_fav_lang()[1]]
    print(all_interests)
    exists = db.session.query(db.exists().where(Interest.interest_id == current_user.id)).scalar()
    if not exists:
        return redirect(url_for('add_interests'))

    return render_template('home.html', users_stack=users_stack, all_interests=all_interests, interests=interests)

@app.route("/about")
@login_required
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                firstname=form.firstname.data, lastname=form.lastname.data, date_of_birth=form.date_of_birth.data)
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  #checks if user is logged in
        return redirect(url_for('home'))    #redirect to the home page
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  #The result of filter_by() is a query that only includes the objects that have a matching username. complete query by calling first(), returns the user object if it exists,None if it does not.
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/account")
@login_required
#Allows a user to view their account profile only if they are logged in
def account():

    selected_interests = []

    user_interests = Interest.query.filter_by(interest_id=current_user.id).first()

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

    selected_interests.append(fav_lang.fav_lang_name)
    selected_interests.append(second_fav_lang.fav_lang_name)
    selected_interests.append(database_knowledge.database_knowledge_name)
    selected_interests.append(fav_database_system.fav_database_system_name)
    selected_interests.append(field_interest.field_interest_name)
    selected_interests.append(programmer_type.programmer_type_name)
    selected_interests.append(experience.experience_name)

    return render_template('account.html', title='Account', selected_interests=selected_interests)

@app.route("/profile/<user>", methods=['GET', 'POST'])
@login_required
#Allows a user to view other user's profile page
def profile(user):

    selected_user=User.query.filter_by(username=user).first()
    user = selected_user.username

    userid=selected_user.id

    selected_interests = []

    user_interests = Interest.query.filter_by(interest_id=userid).first()

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

    selected_interests.append(fav_lang.fav_lang_name)
    selected_interests.append(second_fav_lang.fav_lang_name)
    selected_interests.append(database_knowledge.database_knowledge_name)
    selected_interests.append(fav_database_system.fav_database_system_name)
    selected_interests.append(field_interest.field_interest_name)
    selected_interests.append(programmer_type.programmer_type_name)
    selected_interests.append(experience.experience_name)

    return render_template('profile.html', selected_user=selected_user, user=user, selected_interests=selected_interests)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        if form.profilepic.data:
            picture_file = save_picture(form.profilepic.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        flash('Your photo has been uploaded! It is now your profile pic', 'success')
    image_file = url_for('static', filename='profilepics/' + current_user.image_file)
    return render_template('profileform.html', title='Edit Profile', form=form, image_file=image_file)

@app.route('/add_interests', methods=['GET', 'POST'])
@login_required
def add_interests():
    #form = InterestForm()
    all_interests = [all_fav_programming_lang(), all_second_fav_lang(),all_database_knowledge(),all_fav_database_systems(),all_field_interests(),
    all_programmer_types(),all_experience_level()]

    user_id = current_user.id
    fav_lang_id = request.form.get("Your Favorite Programming Language")
    second_lang_id = request.form.get("Second Favourite Programming Language")
    database_knowledge_id = request.form.get("Choose Your Speciality Database Knowledge")
    fav_database_system_id = request.form.get('Favorite Database Management System')
    field_interest_id = request.form.get('Your Field Of Interest')
    programmer_type_id = request.form.get('Which Statement Below Describes You Most Accurately')
    experience_id = request.form.get('What is Your Experience Level')

    if request.method == 'POST':
          #add user interests for the specific user
        interest = Interest(
            user_id=user_id,
            fav_programming_lang_id=fav_lang_id,
            second_fav_lang_id=second_lang_id,
            database_knowledge_id=database_knowledge_id,
            fav_database_system_id=fav_database_system_id,
            field_interest_id=field_interest_id,
            programmer_type_id=programmer_type_id,
            experience_id=experience_id
        )

        db.session.add(interest)
        db.session.commit()
        return redirect(url_for('account'))

    print(all_interests)


    return render_template('interestform.html', title='Add Interests', all_interests=all_interests)

@app.route('/edit_interests', methods=['GET', 'POST'])
@login_required
def edit_interests():

    all_interests = [all_fav_programming_lang(), all_second_fav_lang(),all_database_knowledge(),all_fav_database_systems(),all_field_interests(),
    all_programmer_types(),all_experience_level()]

    user_id = current_user.id
    fav_lang_id = request.form.get("Your Favorite Programming Language")
    second_lang_id = request.form.get("Second Favourite Programming Language")
    database_knowledge_id = request.form.get("Choose Your Speciality Database Knowledge")
    fav_database_system_id = request.form.get('Favorite Database Management System')
    field_interest_id = request.form.get('Your Field Of Interest')
    programmer_type_id = request.form.get('Which Statement Below Describes You Most Accurately')
    experience_id = request.form.get('What is Your Experience Level')

    user_interest = Interest.query.filter_by(interest_id=user_id).first()

    if request.method == 'POST':
        #find the user interest corresponding to the user_id
        #edit that interest
        user_interest.fav_programming_langid = fav_lang_id
        user_interest.second_fav_lang_id = second_lang_id
        user_interest.database_knowledge_id = database_knowledge_id
        user_interest.fav_database_system_id = fav_database_system_id
        user_interest.field_interest_id = field_interest_id
        user_interest.programmer_type_id = programmer_type_id
        user_interest.experience_id = experience_id

        db.session.commit()
        return redirect(url_for('account'))

    return render_template('editinterests.html', title='Edit Interests', all_interests=all_interests)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profilepics', picture_fn)

    output_size = (568, 528)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    recipient = user
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(sender=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
        flash('Your message has been sent.')
        
        return redirect(url_for('profile', user=recipient.username))
    return render_template('send_message.html', title='Send Message',
                           form=form, recipient=recipient)

@app.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)
    
    next_url = url_for('messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('messages.html', messages=messages.items,
                           next_url=next_url, prev_url=prev_url)

@app.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])
