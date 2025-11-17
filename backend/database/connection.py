import os
import psycopg2
from urllib.parse import urlparse, parse_qs

def get_db_connection():
    db_url = os.getenv("DATABASE_URL")

    if not db_url:
        raise Exception("DATABASE_URL not found")

    url = urlparse(db_url)

    # Extract SSL mode if present
    query = parse_qs(url.query)
    ssl_mode = query.get("sslmode", ["require"])[0]

    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port,
        sslmode=ssl_mode   # <-- important
    )
    return conn
