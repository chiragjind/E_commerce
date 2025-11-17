import os
import psycopg2
from urllib.parse import urlparse

def get_db_connection():
    db_url = os.getenv("DATABASE_URL")

    if not db_url:
        raise Exception("DATABASE_URL not found")

    url = urlparse(db_url)

    conn = psycopg2.connect(
        database=url.path[1:],  
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    return conn
