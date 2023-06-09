import os

import mariadb

from flask import Flask, render_template

if not os.environ.get("DB_USER") or not os.environ.get("DB_PASS"):
    raise RuntimeError("Database authentication not given")

try:
    conn = mariadb.connect(
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASS"),
        host="localhost",
        port=3306,
        database="test"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cur = conn.cursor()

app = Flask(__name__)

@app.route("/")
def hello_world():

    return "<p>Hello, World!</p>"