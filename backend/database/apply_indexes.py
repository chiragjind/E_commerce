import psycopg2
from database.connection import get_db_connection

def apply_indexes():
    """
    Apply all required B-tree indexes to optimize query performance.
    Makes resume bullet fully accurate.
    """
    print("Connecting to database...")
    conn = get_db_connection()
    cur = conn.cursor()

    print("Applying database indexes...")

    # Index for faster interaction lookup by user_id
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_interactions_user 
        ON interactions(user_id);
    """)

    # Index for faster interaction lookup by product_id
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_interactions_product 
        ON interactions(product_id);
    """)

    # Index for faster username lookup (login)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_users_username 
        ON users(username);
    """)

    conn.commit()
    cur.close()
    conn.close()

    print("Indexes applied successfully!")

if __name__ == "__main__":
    apply_indexes()
