from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "bornbeautiful2026"

#database
def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS booksing(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT NOT NULL,
            phone TEXT NOT NULL,
            sercive TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            notes TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )   
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    admin = conn.execute("SELECT * FROM admin WHERE username = 'admin'").fetchone()
    if not admin:
        conn.execute("INSERT INTO admin (username, password) VALUES ('admin', 'bornbeautiful2026')")
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/book", methods=["GET", "POST"])
def book():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        service = request.form.get("service")
        date = request.form.get("date")
        time = request.form.get("time")
        notes = request.form.get("notes")

        conn = get_db()
        conn.execute("""
            INSERT INTO booksing (name, phone, service, date, time, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, phone, service, date, time, notes))
        conn.commit()
        conn.close()

        msg = f"New Booking!%0AName: {name}%0APhone: {phone}%0AService: {service}%0ADate: {date}%0ATime: {time}%0ANotes: {notes}"
        whatsapp_url = f"https://wa.me/60168783226?text={msg}"


        flash("Booking submitted successfully!", "success")
        return redirect(whatsapp_url)

    return render_template('book.html')
