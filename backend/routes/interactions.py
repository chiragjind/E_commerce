from flask import Blueprint, request, jsonify
from database.connection import get_db_connection

interactions_bp = Blueprint('interactions', __name__)

@interactions_bp.route('/interactions', methods=['POST'])
def add_interaction():
    data = request.json

    user_id = data.get("user_id")
    product_id = data.get("product_id")
    action = data.get("action")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO interactions (user_id, product_id, action) VALUES (%s, %s, %s);",
        (user_id, product_id, action)
    )
    conn.commit()

    return jsonify({"message": "Interaction saved"}), 201
