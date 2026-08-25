import os
import time
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    return psycopg.connect(DATABASE_URL)

def init_db():
    retries = 5
    while retries > 0:
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    # 1. Create table
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS tasks (
                            id SERIAL PRIMARY KEY,
                            title TEXT,
                            done BOOLEAN
                        );
                    """)
                    
                    # 2. Count existing rows
                    cur.execute("SELECT COUNT(*) FROM tasks;")
                    count = cur.fetchone()[0]

                    # 3. Seed only if empty
                    if count == 0:
                        cur.execute("""
                            INSERT INTO tasks (title, done) VALUES
                            ('Task 1', false),
                            ('Task 2', false),
                            ('Task 3', false);
                        """)
                    conn.commit()
            print("Database initialized successfully.")
            break
        except psycopg.OperationalError:
            retries -= 1
            print("PostgreSQL is starting up, retrying connection in 2 seconds...")
            time.sleep(2)