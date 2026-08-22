import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

conn = psycopg.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

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
conn.close()
print("Done.")