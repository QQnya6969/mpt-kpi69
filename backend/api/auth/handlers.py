import bcrypt
from flask import Blueprint, jsonify, request, url_for
from flask_login import login_user, logout_user
from flask_mail import Message
import jwt
import datetime
import secrets

from extensions import db, mail
from models import User

auth_bp = Blueprint("auth", __name__)
SECRET_KEY = secrets.token_hex(32)  #Генерация ключа, мб поместить в другое место

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()
    if user and bcrypt.checkpw(data["password"].encode('utf-8'), user.user_passhash.encode('utf-8')):
        login_user(user)
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"}), 200

@auth_bp.route("/reset_password", methods=["POST"])
def reset_password():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    #создаем токен
    token = jwt.encode({
        "sub": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1) #время действия токена 1 час
    }, SECRET_KEY, algorithm="HS256")
    reset_url = url_for("auth.complete_reset", token=token, _external=True)

    msg = Message("Password Reset Request", recipients=[user.email])
    msg.body = f"To reset your password, visit the following link: {reset_url}"
    mail.send(msg)

    return jsonify({"message": "Reset link sent"}), 200

@auth_bp.route("/reset_password/<token>", methods=["POST"])
def complete_reset(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=["HS256"])
        user_id = payload["sub"]
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 400
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 400
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Invalid token"}), 400

    data = request.json
    user.set_password(data["password"])
    db.session.commit()
    return jsonify({"message": "Password reset successful"}), 200