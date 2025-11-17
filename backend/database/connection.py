import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    conn = psycopg2.connect(
         host="db",
        database="mini_reco_db",
        user="postgres",
        password="Chiragiit@123"
    )
    return conn
