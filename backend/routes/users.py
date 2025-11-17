from flask import Blueprint, request, jsonify
from database.connection import get_db_connection

users_bp = Blueprint('users', __name__)

@users_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get("username")

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id;", (username,))
        user_id = cur.fetchone()[0]
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400

    return jsonify({"message": "User created", "user_id": user_id}), 201


@users_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE username = %s;", (username,))
    user = cur.fetchone()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "Login successful", "user_id": user[0]})
