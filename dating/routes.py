import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, current_app, jsonify
from dating import app, db, bcrypt
from dating.forms import RegistrationForm, LoginForm, EditProfileForm, MessageForm
from dating.models import *
from flask_login import login_user, current_user, logout_user, login_required
from dating.queries import *
from dating.matcher import *
import datetime


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
    fav_lang_id = request.form.get("Favorite programming languages")
    second_lang_id = request.form.get("Second favourite programming language")
    database_knowledge_id = request.form.get("Database knowledge")
    fav_database_system_id = request.form.get('Favorite database systems')
    field_interest_id = request.form.get('Field interests')
    programmer_type_id = request.form.get('Programmer types')
    experience_id = request.form.get('Experience levels')

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

def clean_time(str_tme):
    """ Helper function to clean a string that comes from the html date input """

    chars = str_tme.split('T')
    tm = (" ").join(chars)
    return tm + ":00"

@app.route('/generate_matches', methods=["GET"])
@login_required
def show_generate_matches_form():
    """Route for users to enter their zipcode and a time for meeting up!!.
    """

    return render_template("generate_matches.html")

@app.route('/generate_matches', methods=["POST"])
@login_required
def generate_matches():
    """This route
    - gets the time from the user who is logged in
    - gets the zipcode from the user
    """

    query_time = request.form.get('triptime')
    query_pin_code = request.form.get('pincode')
    user_id = session['user_id']
    #if this user is in the database for the same exact date, then go to show_matches
    session['query_pincode'] = query_pin_code
    session_time = clean_time(query_time)
    session['query_time'] = session_time

    date_out = datetime.datetime(*[int(v) for v in query_time.replace('T', '-').replace(':', '-').split('-')])

    trip =  PendingMatch(user_id=user_id,
                        query_pin_code=query_pin_code,
                        query_time=date_out,
                        pending=True)

    db.session.add(trip)
    db.session.commit()

    #at this point we will pass the information the yelper
    #yelper will end information to google and google will render
    # a map with relevant information

    return redirect("show_matches")

@app.route('/show_matches',methods=['GET'])
@login_required
def show_potential_matches():
    """ This route
        - accesses the session for a user_id and query_pin_code
        - accesses the matchmaker module for making matches
        -
    """

    # gets the user_id from the session
    userid = current_user.id
    # gets the pincode from the session
    pin = session.get('query_pincode')
    # gets the query_time from the session
    query_time = session.get('query_time')
    # gets a list of pending matches using the potential_matches from
    # the queries module
    # potential_matches is  a list of user_ids
    # => [189, 181, 345, 282, 353, 271, 9, 9, 501, 9]
    potential_matches = find_valid_matches(userid, pin, query_time)

    # gets a list of tuples of match percents for the userid
    # uses the create_matches from the matchmaker
    # create_matches takes a list of user_ids as the first param
    # create_matches take the userid as the second param
    # create_matches([30,40,50],60)
    # => [(60, 30, 57.90407177363699), (60, 40, 54.887163561076605)]
    match_percents = create_matches(potential_matches, userid)

    user_info = get_user_info(userid)
    # this is the logged in user's info
    user_name = get_user_name(userid)
    # this is the logged in user's username

    match_info = []

    for user in match_percents:
        matched_user_id = user[1]
        matched_username = get_user_name(matched_user_id)
        user_info = get_user_info(matched_user_id)
        match_percent = round(user[2])
        #match_details = get_commons(user[1], userid)

        match_info.append((matched_username, match_percent,
                        matched_user_id, user_info))

    # match info is a list of tuples [(username,
    #                               match_percent,
    #                               matched_user_id,
    #                                user_info, match_details)]


    return render_template('show_matches.html',
                                user_name=user_name,
                                user_info=user_info,
                                match_info=match_info)

@app.route('/show_matches', methods=["POST"])
@login_required
def update_potential_matches():
    """ - Gets the user input for a confirm match
        - Updates the user input for a match to the db
    """

    matched = request.form.get("user_match")
    user_id_1 = current_user.id
    match_date = datetime.datetime.now()
    query_pincode = session['query_pincode']
    session['matched_user'] = matched

    successfulmatch = UserMatch.query.filter_by(user_id_1 = current_user.id).first()
    if successfulmatch is not None:
        if successfulmatch.user_id_2 == matched:
            return redirect(url_for('show_potential_matches'))


    match = UserMatch(user_id_1=user_id_1,
                        user_id_2=matched,
                        match_date=match_date,
                        user_2_status=False,
                        query_pincode=query_pincode)

    db.session.add(match)
    db.session.commit()

    return redirect(url_for('confirmed'))

@app.route('/match_console', methods=["POST"])
@login_required
def show_match_details():
    """ This route
        - displays the final match of user's choice
        - shows all the common interests to the user
        - gives the user a chance to message the match
        - gives the user a chance to choose a coffee shop
    """

    userid1 = current_user.id
    userid2 = request.form.get("match_details")
    user_info1 = get_user_info(userid1)
    username1 = get_user_name(userid1)
    user_info2 = get_user_info(userid2)
    username2 = get_user_name(userid2)
    match_info = get_commons(userid1, userid2)
    match_percent = round(make_match(userid1, userid2))

    return render_template("match_console.html", user_info1=user_info1,
                                                    username1=username1,
                                                    username2=username2,
                                                    user_info2=user_info2,
                                                    match_info=match_info,
                                                    match_percent=match_percent)

@app.route("/confirmed", methods=['GET'])
@login_required
def confirmed():
    return render_template('confirmed.html')



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
        return redirect(url_for('show_potential_matches', username=recipient))
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
