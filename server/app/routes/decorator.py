from functools import wraps
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import jsonify
from app.models import User

def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({"error": "Invalid token"}), 401

        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            return jsonify({"error": "Invalid token identity"}), 401

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 401

        if user.role != 1:
            return jsonify({"error": "Admin privilege required"}), 403
        return fn(*args, **kwargs)
    return wrapper
