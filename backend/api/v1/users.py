from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from functools import wraps

from extensions import db
from models import Position, User

users_bp = Blueprint("users", __name__)

def require_role(role_name):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Проверяем, авторизован ли пользователь
            if not current_user.is_authenticated:
                return jsonify({"error": "Unauthorized"}), 401

            # Проверяем, есть ли у пользователя нужная роль
            if current_user.role.name != role_name:
                return jsonify({"error": "Access denied"}), 403

            # Если проверка прошла, вызываем функцию
            return f(*args, **kwargs)

        return wrapped

    return decorator

@users_bp.route("/users", methods=["GET", "POST"])
@login_required
def users():
    if request.method == "GET":
        users = User.query.all()
        return jsonify([{"id": u.id, "email": u.email} for u in users])
    elif request.method == "POST":

        # Используем новый декоратор для проверки роли
        @require_role("admin")
        def create_user():
            data = request.json
            user = User(
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                role_id=2  # Предположим, что role_id=2 соответствует роли "user"
            )
            db.session.add(user)
            db.session.commit()
            return jsonify({"message": "User created"}), 201

        return create_user()

@users_bp.route("/positions", methods=["GET", "POST"])
@login_required
@require_role("admin")  # Используем декоратор для проверки роли
def positions():
    if request.method == "GET":
        positions = Position.query.all()
        return jsonify([{"id": p.id, "name": p.name} for p in positions])
    elif request.method == "POST":
        data = request.json
        position = Position(name=data["name"], score_threshold=data["score_threshold"])
        db.session.add(position)
        db.session.commit()
        return jsonify({"message": "Position created"}), 201



