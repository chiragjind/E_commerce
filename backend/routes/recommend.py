from flask import Blueprint, jsonify
from database.connection import get_db_connection
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
import pickle

recommend_bp = Blueprint('recommend', __name__)

# Load XGBoost model
xgb_model = XGBRegressor()
xgb_model.load_model("models/xgb_model.json")

# Load Neural Network model
with open("models/nn_model.pkl", "rb") as f:
    nn_model = pickle.load(f)

@recommend_bp.route('/recommend/<int:user_id>', methods=['GET'])
def recommend(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Get all products
    cur.execute("SELECT id, name, category, price FROM products;")
    products = cur.fetchall()

    # Prepare data for prediction
    product_ids = [p[0] for p in products]
    
    X_pred = pd.DataFrame({
        "user_id": [user_id] * len(product_ids),
        "product_id": product_ids
    })

    # Predict scores using both models
    xgb_scores = xgb_model.predict(X_pred)
    nn_scores = nn_model.predict(X_pred)

    # Weighted score = 0.6 * XGBoost + 0.4 * Neural Net
    final_scores = 0.6 * xgb_scores + 0.4 * nn_scores

    # Sort products by final score
    ranked = sorted(
        zip(products, final_scores),
        key=lambda x: x[1],
        reverse=True
    )

    # Prepare JSON response
    result = []
    for p, score in ranked:
        result.append({
            "id": p[0],
            "name": p[1],
            "category": p[2],
            "price": p[3],
            "score": float(score)
        })

    return jsonify({"recommended": result})
