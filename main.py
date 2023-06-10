import os
import sys

import mariadb

from flask import Flask, render_template, request

if not os.environ.get("DB_USER") or not os.environ.get("DB_PASS"):
    raise RuntimeError("Database authentication not given")

try:
    conn = mariadb.connect(
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASS"),
        host="localhost",
        port=3306,
        database="kereta"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cur = conn.cursor()

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/jadwal", methods=["GET", "POST"])
def jadwal():
    if request.method == "POST":
        stasiun_asal = request.form.get("stasiun_asal")

        cur.execute("""SELECT kk.kode_keberangkatan, s1.nama_stasiun,
                        s2.nama_stasiun, waktu_keberangkatan, waktu_tiba
                        FROM keberangkatan k
                        JOIN kode_keberangkatan kk
                        ON k.kode_keberangkatan=kk.kode_keberangkatan
                        JOIN stasiun s1
                        ON s1.kode_stasiun=kk.kode_stasiun_awal
                        JOIN stasiun s2
                        ON s2.kode_stasiun=kk.kode_stasiun_akhir
                        WHERE s1.nama_stasiun=?
                    """, (stasiun_asal,))

        jadwal_rs = list(cur)

        return render_template("jadwal_result.html",
            stasiun_asal=stasiun_asal,
            jadwal_rs=jadwal_rs
        )

    cur.execute("SELECT nama_stasiun FROM stasiun")

    return render_template("jadwal_form.html", stasiun_rs=list(cur))

@app.route("/stasiun")
def stasiun():
    cur.execute("""SELECT nama_stasiun, count(kk.kode_keberangkatan) from stasiun s
                    LEFT JOIN kode_keberangkatan kk
                    ON kk.kode_stasiun_awal=s.kode_stasiun
                    group by s.kode_stasiun;
                """)

    return render_template("stasiun.html", stasiun_rs=list(cur))

@app.route("/masinis")
def masinis():
    cur.execute("SELECT * FROM masinis")

    return render_template("masinis.html", masinis_rs=list(cur))

@app.route("/tentang")
def tentang():
    return render_template("tentang.html")
