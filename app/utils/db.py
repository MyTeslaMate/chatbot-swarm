import psycopg2
from psycopg2 import sql
import os

def query_db(query):
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    cur = conn.cursor()
    try:
        query = sql.SQL(query)
        cur.execute(query)
        rows = cur.fetchall()
        return {"response": {"rows": rows}}
    except Exception as e:
        return {"response": {"error": str(e)}}
    finally:
        cur.close()
        conn.close()