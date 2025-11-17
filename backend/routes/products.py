from flask import Blueprint, request, jsonify
from database.connection import get_db_connection

products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cur = conn.cursor()

    # ------ Pagination parameters ------
    page = int(request.args.get("page", 1))        # default page = 1
    limit = int(request.args.get("limit", 20))     # default limit = 20
    offset = (page - 1) * limit

    # ------ Fetch products with pagination ------
    cur.execute("""
        SELECT id, name, category, price
        FROM products
        ORDER BY id
        LIMIT %s OFFSET %s;
    """, (limit, offset))

    products = cur.fetchall()

    # Format JSON response
    result = [
        {
            "id": p[0],
            "name": p[1],
            "category": p[2],
            "price": p[3]
        }
        for p in products
    ]

    # ------ Total count for frontend ------
    cur.execute("SELECT COUNT(*) FROM products;")
    total_count = cur.fetchone()[0]

    return jsonify({
        "page": page,
        "limit": limit,
        "total_products": total_count,
        "total_pages": (total_count + limit - 1) // limit,
        "data": result
    })
