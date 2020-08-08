from flask import Flask, request, jsonify
from matcher import app

if __name__ == "__main__":
    app.run(debug=True)

# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

# #DB
# db = SQLAlchemy(app)

# class Users(db.Model):
#     id = db.Column('student_id', db.Integer, primary_key = True) # primary_key makes it so that this value is unique and can be used to identify this record.
#     username = db.Column(db.String(24))
#     email = db.Column(db.String(64))
#     pwd = db.Column(db.String(64))

#     # Constructor
#     def __init__(self, username, email, pwd):
#         self.username = username
#         self.email = email
#         self.pwd = pwd


# @app.route("/api/users", methods=["GET", "POST", "DELETE"])
# def users():
#     method = request.method
#     if (method.lower() == "get"): #READ
#         users = Users.query.all()
#         return jsonify([{"id": user.id, "username": user.username, "email": user.email, "password": user.pwd} for user in users]) # Get all values from db
#     elif (method.lower() == "post"): #CREATE
#         try:
#             username = request.json["username"]
#             email = request.json["email"]
#             pwd = request.json["pwd"]
#             if (username and pwd and email):
#                 try:
#                     user = Users(username, email, pwd)
#                     db.session.add(user)
#                     db.session.commit()
#                     return jsonify({"success": True})
#                 except Exception as e:
#                     return ({"error": e})
#             else:
#                 return jsonify({"error": "Invalid Form"})
#         except:
#             return jsonify({"error": "Invalid Form"})
#     elif (method.lower() == "delete"):
#         try:
#             uid = request.json["id"]
#             if (uid):
#                 try:
#                     user = Users.query.get(uid)
#                     db.session.delete(user)
#                     db.session.commit()
#                     return jsonify({"success": True})
#                 except Exception as e:
#                     return jsonify({"error": e})
#             else:
#                 return jsonify({"error": "m"})
#         except:
#             return jsonify({"error": "m"})