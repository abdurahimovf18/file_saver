#!/usr/bin/env python3
import os
import time
import psycopg

DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = int(os.environ.get("DB_PORT", 5432))
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")

while True:
    try:
        with psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME,
        ):
            print("DB is ready!")
            break
    except Exception:
        print("DB not ready yet, retrying in 2s...")
        time.sleep(2)

# Run Alembic migrations
os.system("alembic upgrade head")
