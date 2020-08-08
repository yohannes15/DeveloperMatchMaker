from matcher import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json
from time import time
#The purpose of this field is to hold a hash of the user password, which will be used to verify the password entered
#by the user during the login process. werkzeug is a package that implements password hashing.

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
#Flask-Login knows nothing about databases, it needs the application's help in loading a user.
#configure a user loader function that can be called to load a user given the ID.
#The user loader is registered with Flask-Login with the @login.user_loader decorator.

class User(db.Model, UserMixin):  #This class defines several fields as class variables.
    """ User of the Dating website."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(20), nullable=True, default='default.jpg')

    messages_sent = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='sender', lazy='dynamic')
    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')

    last_message_read_time = db.Column(db.DateTime)
    notifications = db.relationship('Notification', backref='user',
                                    lazy='dynamic')
    #profile_picture = db.Column(db.String(250), default = 'default.jpg', nullable=True)

    def _repr_(self): #The __repr__ method tells Python how to print objects of this class
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()

    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n

class Interest(db.Model):
    """ User interests for matchmaking, Each Column will
    hold integers that correspond to the information on other tables.
    """

    __tablename__ = 'interests'

    interest_id = db.Column(db.Integer, autoincrement=True,
                            primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    fav_programming_lang_id = db.Column(db.Integer,
                            db.ForeignKey('fav_programming_lang.fav_lang_id'),
                            nullable=False)
    second_fav_lang_id = db.Column(db.Integer,
                                db.ForeignKey('second_fav_lang.fav_lang_id'),
                                nullable=False)
    database_knowledge_id = db.Column(db.Integer,
                                db.ForeignKey('database_knowledge.database_knowledge_id'),
                                nullable=False)
    fav_database_system_id = db.Column(db.Integer,
                                db.ForeignKey('fav_database_system.fav_database_system_id'),
                                nullable=False)
    field_interest_id = db.Column(db.Integer,
                        db.ForeignKey('field_interest.field_interest_id'),
                        nullable=False)
    programmer_type_id = db.Column(db.Integer,
                        db.ForeignKey('programmer_type.programmer_type_id'), nullable=False)

    experience_id = db.Column(db.Integer,
                        db.ForeignKey('experience.experience_id'),
                        nullable=False)

    def __repr__ (self):
        """return interest choices of the user"""

        d1 ='< interest_id={a}, fav_programming_lang_id={b},'.format(a=self.interest_id,
                                                        b=self.fav_programming_lang_id)
        d2 =' second_fav_lang_id={c}, database_knowledge_id={d},'.format(c=self.second_fav_lang_id,
                                                        d=self.database_knowledge_id)
        d3 =' fav_database_system_id={e}, field_interest_id={f},'.format(e=self.fav_database_system_id,
                                                        f=self.field_interest_id)
        d4 =' programmer_type_id={g}, experience_id={h},'.format(g=self.programmer_type_id,
                                                        h=self.experience_id)

        return d1 + d2 + d3 + d4 


class FavProgrammingLang(db.Model):
    """"""

    __tablename__ = 'fav_programming_lang'

    fav_lang_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fav_lang_name = db.Column(db.String(40), nullable=False)

    interest = db.relationship('Interest',
                            backref=db.backref('fav_programming_lang'))

    def __repr__ (self):
        """displays the ids of fav programming id and fav programming name
        Can be cross-referenced with the interests table"""

        return'<fav_lang_id={}, fav_lang_name={}>'.format(self.fav_lang_id,
                                                            self.fav_lang_name)


class SecondFavProgrammingLang(db.Model):
    """"""

    __tablename__ = 'second_fav_lang'

    fav_lang_id= db.Column(db.Integer, autoincrement=True,
                                            primary_key=True)
    fav_lang_name = db.Column(db.String(40), nullable=False)

    interest = db.relationship('Interest',
                            backref=db.backref('second_fav_lang'))

    def __repr__(self):
        """displays the ids of second fav programming id and programming name
        Can be cross-referenced with the interests table"""

        return'<fav_lang_id={}, fav_lang_name={}>'.format(self.fav_lang_id,
                                                            self.fav_lang_name)


class DatabaseKnowledge(db.Model):
    """"""

    __tablename__ = 'database_knowledge'

    database_knowledge_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    database_knowledge_name = db.Column(db.String(40), nullable=False)

    interest = db.relationship('Interest',
                            backref=db.backref('database_knowledge'))

    def __repr__ (self):
        """displays the ids of database knowledge id and database name
        Can be cross-referenced with the interests table"""

        return'<mdatabase_knowledge_id={}, database_knowledge_name={}>'.format(self.database_knowledge_id,
                                                            self.database_knowledge_name)


class FavDatabaseSystem(db.Model):

    __tablename__ = 'fav_database_system'

    fav_database_system_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fav_database_system_name= db.Column(db.String(40), nullable=False)

    interest = db.relationship('Interest',
                            backref=db.backref('fav_database_system'))

    def __repr__ (self):
        """displays the ids of fav database system and database names
        Can be cross-referenced with the interests table"""

        return'<fav_database_system_id={}, fav_database_system_name={}>'.format(self.fav_database_system_id,
                                                                self.fav_database_system_name)


class FieldInterest(db.Model):

    __tablename__ = 'field_interest'

    field_interest_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    field_interest_name= db.Column(db.String(40), nullable=False)

    interest = db.relationship('Interest',
                            backref=db.backref('field_interest'))

    def __repr__ (self):
        """displays the ids of field of interest and names
        Can be cross-referenced with the interests table"""

        return'<field_interest_id={}, field_interest_name={}>'.format(self.field_interest_id,
                                                    self.field_interest_name)



class ProgrammerType(db.Model):

    __tablename__ = 'programmer_type'

    programmer_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    programmer_type_name = db.Column(db.String(40), nullable=False)

    interest = db.relationship('Interest',
                            backref=db.backref('programmer_type'))

    def __repr__ (self):
        """displays the ids of programmer type and names
        Can be cross-referenced with the interests table"""

        return'<programmer_type_id={}, programmer_type_name={}>'.format(self.programmer_type_id,
                                                        self.programmer_type_name)


class ExperienceLevel(db.Model):

    __tablename__ = 'experience'

    experience_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    experience_name = db.Column(db.String(40), nullable=False)

    interest = db.relationship('Interest',
                            backref=db.backref('experience'))

    def __repr__ (self):
        """displays the ids of experience, and years of experience
        Can be cross-referenced with the interests table"""

        return'<experience_id={}, experience_name={}>'.format(self.experience_id,
                                                            self.experience_name)


class Message(db.Model):

    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.body)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))
