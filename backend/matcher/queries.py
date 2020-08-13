""" This file queries databases """

from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from matcher.models import *
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


# def validate_password(input_email, input_password):
#     """ Queries the users table and accepts email and password as inputs for validation"""

#     user = User.query.filter(User.email == '{}'.format(input_email)).first()
#     password = user.password
#     email = user.email

#     return password == input_password and email == input_email

def get_max_id(input_table_id):
    """ Queries a given table.
        Returns a max count for the primary key of the given table.
    """

    max_id = db.session.query(func.max(input_table_id)).one()
    return int(max_id[0])

def all_fav_programming_lang():
    """ Queries the fav_programming_lang table.Returns a list of tuples, first element is the programming lang id and second
        element is the name."""
    fav_prog_lang_schema = FavProgrammingLangSchema(many=True)
    programming_langs = FavProgrammingLang.query.all()
    
    json_fav_lang = fav_prog_lang_schema.dumps(programming_langs)
    json_fav_lang = json.loads(json_fav_lang)

    fav_programming_lang = []

    return ["Your Favorite Programming Language", json_fav_lang, 'fav_lang_']


def all_second_fav_lang():
    """ Queries the second_fav_lang table.Returns a list of tuples, first element is the second_fav_lang id and second
        element is the name."""
    
    second_fav_prog_lang_schema = SecondFavProgrammingLangSchema(many=True)
    programming_langs = SecondFavProgrammingLang.query.all()
    
    json_second_fav_lang = second_fav_prog_lang_schema.dumps(programming_langs)
    json_second_fav_lang = json.loads(json_second_fav_lang)

    return ["Second Favourite Programming Language", json_second_fav_lang, 'fav_lang_']


def all_database_knowledge():
    """ Queries the database_knowledge table. Returns a list of tuples, first element is the database_knowledge id and second
        element is the name.
    """
    database_schema = DatabaseKnowledgeSchema(many=True)
    databases = DatabaseKnowledge.query.all()
    
    json_databases = database_schema.dumps(databases)
    json_databases = json.loads(json_databases)

    return ["Choose Your Speciality Database Knowledge", json_databases, "database_knowledge_"]

def all_fav_database_systems():
    """ Queries the fav_database_system table. Returns a list of tuples, first element is the fav_database_system id and second
        element is the name.
    """
    database_systems_schema = FavDatabaseSystemSchema(many=True)
    database_systems = FavDatabaseSystem.query.all()

    json_db_systems = database_systems_schema.dumps(database_systems)
    json_db_systems = json.loads(json_db_systems)

    return ["Favorite Database Management System", json_db_systems, "fav_database_system_"]


def all_field_interests():
    """ Queries the field_interest table.Returns a list of tuples, first element is the field_interest id and second
        element is the name.
    """
    field_interest_schema = FieldInterestSchema(many=True)
    field_interests = FieldInterest.query.all()
    json_fields = field_interest_schema.dumps(field_interests)

    json_fields = json.loads(json_fields)

    return ["Your Field Of Interest", json_fields, "field_interest_"]

def all_programmer_types():
    """ Queries the programmer_type table. Returns a list of tuples, first element is the programmer_type id and second
        element is the description.
    """
    programmer_schema = ProgrammerTypeSchema(many=True)
    types = ProgrammerType.query.all()
    json_types = programmer_schema.dumps(types)

    json_types = json.loads(json_types)

    return ["Which Statement Below Describes You Most Accurately", json_types, "programmer_type_"]


def all_experience_level():
    """ Queries the experience table. Returns a list of tuples, first element is the experience id and second
        element is the description.
    """
    exp_level_schema = ExperienceLevelSchema(many=True)
    exp_levels = ExperienceLevel.query.all()
    json_exp_levels = exp_level_schema.dumps(exp_levels)

    json_exp_levels = json.loads(json_exp_levels)

    return ["What is Your Experience Level", json_exp_levels, "experience_"]

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


