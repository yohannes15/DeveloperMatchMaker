""" This file queries databases """

from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from dating.models import *
from functools import wraps
from flask import Flask, render_template, redirect, request, flash, session, g
import datetime



def get_user_id(input_email):

    """ Queries the users table with email as an argument and
        returns the user_id of a user.
    """

    user = User.query.filter(User.email == '{}'.format(input_email)).all()
    user_id = user[0].user_id
    return user_id

def get_user_name(input_id):
    """ Queries the users table and accepts a userid as input.
        Returns the fname and lname of the user.
    """

    user = User.query.filter(User.id == input_id).first()
    username = user.username;
    return username

def get_user_info(input_id):
    """ Queries the users table and accepts a userid as input.
        Returns all the user info as a list
        OUTPUT FORMAT = string.
    """

    user = User.query.filter(User.id == input_id).all()

    user_id = user[0].id
    email = user[0].email
    user_name = user[0].username
    date_of_birth = user[0].date_of_birth
    fname = user[0].firstname
    lname = user[0].lastname
    profile_picture = user[0].image_file


    return [user_id, email, user_name,
            date_of_birth,
            fname, lname, profile_picture]


def get_all_made_matches(user_id):
    """ Queries the user_matches table and accepts a userid as input.
        INPUT FORMAT = Integer.
        Returns a list of tuples with the first element as the user name
        and the second element as the url to the profile picture.
        OUTPUT FORMAT = list of tuples of strings.
    """
    # query the user_matches table
    check_matches = UserMatch.query.filter(UserMatch.user_id_1 == user_id,
                                         UserMatch.user_2_status == True)

    matches = check_matches.all()
    all_match_info = []

    for match in matches:
        user_id2 = match.user_id_2
        user_info = get_user_info(user_id2)
        user_name = user_info[6] + " " + user_info[7]
        all_match_info.append(user_name, user_info[-1])

    return all_match_info

def validate_password(input_email, input_password):
    """ Queries the users table and accepts email and password as inputs for validation"""

    user = User.query.filter(User.email == '{}'.format(input_email)).first()
    password = user.password
    email = user.email

    return password == input_password and email == input_email

def get_max_id(input_table_id):
    """ Queries a given table.
        Returns a max count for the primary key of the given table.
    """

    max_id = db.session.query(func.max(input_table_id)).one()
    return int(max_id[0])

def all_fav_programming_lang():
    """ Queries the fav_programming_lang table.Returns a list of tuples, first element is the programming lang id and second
        element is the name."""

    programming_langs = FavProgrammingLang.query.all()
    fav_programming_lang = []

    for lang in programming_langs:
        fav_programming_lang.append((lang.fav_lang_id, lang.fav_lang_name))

    return ["Your Favorite Programming Language", fav_programming_lang]


def all_second_fav_lang():
    """ Queries the second_fav_lang table.Returns a list of tuples, first element is the second_fav_lang id and second
        element is the name."""


    programming_langs = SecondFavProgrammingLang.query.all()
    second_fav_programming_lang = []

    for lang in programming_langs:
        second_fav_programming_lang.append((lang.fav_lang_id, lang.fav_lang_name))

    return ["Second Favourite Programming Language", second_fav_programming_lang]


def all_database_knowledge():
    """ Queries the database_knowledge table. Returns a list of tuples, first element is the database_knowledge id and second
        element is the name.
    """

    databases = DatabaseKnowledge.query.all()
    database_knowledge = []

    for database in databases:
        database_knowledge.append((database.database_knowledge_id,
                         database.database_knowledge_name))

    return ["Choose Your Speciality Database Knowledge", database_knowledge]

def all_fav_database_systems():
    """ Queries the fav_database_system table. Returns a list of tuples, first element is the fav_database_system id and second
        element is the name.
    """

    database_systems = FavDatabaseSystem.query.all()
    fav_database_systems = []

    for database in database_systems:
        fav_database_systems.append((database.fav_database_system_id, database.fav_database_system_name))

    return ["Favorite Database Management System", fav_database_systems]


def all_field_interests():
    """ Queries the field_interest table.Returns a list of tuples, first element is the field_interest id and second
        element is the name.
    """

    field_interests = FieldInterest.query.all()
    fields = []

    for interest in field_interests:
        fields.append((interest.field_interest_id, interest.field_interest_name))

    return ["Your Field Of Interest", fields]

def all_programmer_types():
    """ Queries the programmer_type table. Returns a list of tuples, first element is the programmer_type id and second
        element is the description.
    """

    types = ProgrammerType.query.all()
    programmer_types = []

    for prog_type in types:
        programmer_types.append((prog_type.programmer_type_id, prog_type.programmer_type_name))

    return ["Which Statement Below Describes You Most Accurately", programmer_types]


def all_experience_level():
    """ Queries the experience table. Returns a list of tuples, first element is the experience id and second
        element is the description.
    """

    exp_levels = ExperienceLevel.query.all()
    experiences = []

    for level in exp_levels:
        experiences.append((level.experience_id,
                               level.experience_name))

    return ["What is Your Experience Level", experiences]

def get_user_interests(user_id):
    """ Queries the interests table and accepts a userid as input.
        Returns an object representing one user interest.
    """

    user = Interest.query.filter(Interest.user_id == user_id).first()
    return user


def get_interest_name(interest_id, table_name):
    """ Queries the interest table, accepts interest_id and name of table as
        a parameter. Returns an object of interest type.
    """

    Interest = table_name.query.filter(Interest.user_id == user_id).first()

def get_interest_info(interest_info):
    """ Accepts a SINGLE tuple of INPUT FORMAT: (int, int)
        The first element of the tuple is the value of the interest.
        The second element is the table id.
        Assigns the queries to a small dictionary in this order:
            user.interest_id             |(0)
            user.fav_lang_id             |(1)
            user.fav_lang_id 2           |(2)
            user.database_knowledge_id   |(3)
            user.fav_database_system_id  |(4)
            user.field_interest_id       |(5)
            user.programmer_type_id      |(6)
            user.experience_id           |(7)
    """

    common_value = interest_info[0]
    table_id = interest_info[1]

    id_info = { 1 : FavProgrammingLang.query.filter(FavProgrammingLang.fav_lang_id == common_value),
                2 : SecondFavProgrammingLang.query.filter(SecondFavProgrammingLang.fav_lang_id == common_value),
                3 : DatabaseKnowledge.query.filter(DatabaseKnowledge.database_knowledge_id == common_value),
                4 : FavDatabaseSystem.query.filter(FavDatabaseSystem.fav_database_system_id == common_value),
                5 : FieldInterest.query.filter(FieldInterest.field_interest_id == common_value),
                6 : ProgrammerType.query.filter(ProgrammerType.programmer_type_id == common_value),
                7 : ExperienceLevel.query.filter(ExperienceLevel.experience_id == common_value) }

    interest_details = id_info[table_id].first()

    return interest_details

def get_user_match(user_id):
    """ Queries the user_matches table and accepts a user id as input.
        Returns a list of confirm matches for the specific user.
    """

    q1 = UserMatch.query
    fil = q1.filter(UserMatch.user_id_2 == 339, UserMatch.user_2_status == False).all()



def find_valid_matches(user_id_1, pincode, query_time):
    """ Queries the pending_match for pending matches.
        returns a list of pending match user user_ids.
    """
    potential_matches = []
    # creates an object from the input date string

    # finding matches for the same query time
    query_time_obj = datetime.datetime.strptime(query_time, "%Y-%m-%d %H:%M:%S")

    # check for all pending_matches
    match_q = PendingMatch.query.filter(PendingMatch.query_pin_code == pincode,
                                        func.date(PendingMatch.query_time) == query_time_obj.date(),
                                        PendingMatch.pending == True)

    users = match_q.all()

    for i in users:
        user_id = i.user_id
        potential_matches.append(user_id)

    return potential_matches
