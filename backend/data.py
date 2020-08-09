"""file to seed data from generated data in seed_data into sqlite database"""
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from matcher.models import *
from random import choice
import datetime
from matcher import bcrypt
#import pdb; pdb.set_trace()

def load_users():
    """Load users from static/user_data.txt into database."""

    print ("User")
    User.query.delete()

    file = open("seed_data/user_data.txt")
    for row in file:
        row = row.rstrip()
        row = row.split("|")

        user_id = row[0]
        fname = row[1]
        lname = row[2]
        email = row[3]
        user_name = row[4]
        password = row[5]
        date_of_birth = row[6]
        zipcode = row[7]
        phone = row[8]
        profile_picture = row[10]

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        #insert user
        user = User(id=user_id,
                    firstname=fname,
                    lastname=lname,
                    email=email,
                    username=user_name,
                    password=hashed_password,
                    date_of_birth=date_of_birth,
                    city=zipcode,
                    phone=phone,
                    image_file=profile_picture)

        db.session.add(user)

    db.session.commit()


def load_fav_programming_languages():
    """Load langs from fav_programming_languages into database."""

    print ("FavProgrammingLang")

    #read book_genre_data
    for row in open("seed_data/fav_programming_lang.txt"):
        row = row.rstrip()
        fav_lang_id, fav_lang_name = row.split("|")
        # insert book genre
        lang = FavProgrammingLang(fav_lang_id=fav_lang_id,
                          fav_lang_name=fav_lang_name)

        db.session.add(lang)

    db.session.commit()


def load_second_favorite_programming_language():
    """Load langs from 2nd favorite programming languages into database."""

    print ("SecondFavProgrammingLang")

    for row in open("seed_data/second_fav_lang.txt"):
        row = row.rstrip()
        fav_lang_id, fav_lang_name = row.split("|")
        #insert movie
        lang = SecondFavProgrammingLang(fav_lang_id=fav_lang_id,
                          fav_lang_name=fav_lang_name)

        db.session.add(lang)

    db.session.commit()


def load_database_knowledge():
    """Load types of database knowledge into database."""

    print ("DatabaseKnowledge")

    for row in open("seed_data/database_knowledge.txt"):
        row = row.rstrip()
        database_knowledge_id, database_knowledge_name = row.split("|")
        #insert music
        database = DatabaseKnowledge(database_knowledge_id=database_knowledge_id,
                          database_knowledge_name=database_knowledge_name)

        db.session.add(database)

    db.session.commit()



def load_database_systems():
    """Load fav database systems to database."""

    print ("FavDatabaseSystem")

    for row in open("seed_data/fav_database_system.txt"):
        row = row.rstrip()
        fav_database_system_id, fav_database_system_name = row.split("|")
        #insert cuisine
        databaseSystem = FavDatabaseSystem(fav_database_system_id=fav_database_system_id,
                          fav_database_system_name=fav_database_system_name)

        db.session.add(databaseSystem)

    db.session.commit()


def load_field_interests():
    """Load Fields of Interest into database."""

    print ("FieldInterest")

    for row in open("seed_data/field_interest.txt"):
        row = row.rstrip()
        field_interest_id, field_interest_name = row.split("|")
        #insert hobby
        field = FieldInterest(field_interest_id=field_interest_id,
                         field_interest_name=field_interest_name)

        db.session.add(field)

    db.session.commit()




def load_programmer_types():
    """Load  programmer types into database."""

    print ("ProgrammerType")

    for row in open("seed_data/programmer_type.txt"):
        row = row.rstrip()
        programmer_type_id, programmer_type_name = row.split("|")
        #insert religion
        programmerType = ProgrammerType(programmer_type_id=programmer_type_id,
                            programmer_type_name=programmer_type_name)

        db.session.add(programmerType)

    db.session.commit()



def load_experience_level():
    """Load experience levels into database."""

    print ("ExperienceLevel")

    for row in open("seed_data/programming_experience.txt"):
        row = row.rstrip()
        experience_id, experience_name = row.split("|")
        #insert outdoor
        level = ExperienceLevel(experience_id=experience_id,
                              experience_name=experience_name)

        db.session.add(level)

    db.session.commit()




if __name__ == "__main__":
    from flask import Flask
    from matcher import app
    SQLAlchemy(app)

    # Import different types of data
    load_fav_programming_languages()
    load_second_favorite_programming_language()
    load_database_knowledge()
    load_database_systems()
    load_field_interests()
    load_programmer_types()
    load_experience_level()
