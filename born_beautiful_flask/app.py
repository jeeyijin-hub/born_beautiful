from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_compress import Compress
import os


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-key-only")
Compress(app)

#database
def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS bookings(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT NOT NULL,
            phone TEXT NOT NULL,
            service TEXT NOT NULL,
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
    admin_password = os.environ.get("ADMIN_PASSWORD", "bornbeautiful2026")
    if not admin:
        conn.execute("INSERT INTO admin (username, password) VALUES (?, ?)", ('admin', generate_password_hash(admin_password)))

    else:
        conn.execute("UPDATE admin SET password = ? WHERE username = 'admin'",(generate_password_hash(admin_password),))
        
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/book", methods=["GET", "POST"])
def book():
    if request.method == "POST":
        name    = request.form.get("name")
        phone   = request.form.get("phone")
        service = request.form.get("service")
        date    = request.form.get("date")
        time    = request.form.get("time")
        notes   = request.form.get("notes")

        # date validation
        from datetime import date as date_type
        today = date_type.today().isoformat()
        if date < today:
            flash("Please select a future date.", "danger")
            return render_template("book.html", today=today, form_data=request.form)

        # time slot validation
        conn = get_db()
        existing = conn.execute("""
            SELECT * FROM bookings 
            WHERE date = ? AND time = ? AND status != 'cancelled'
        """, (date, time)).fetchone()

        if existing:
            conn.close()
            flash("This time slot is already booked. Please choose a different time.", "danger")
            return render_template("book.html", today=today, form_data=request.form)

        conn.execute("""
            INSERT INTO bookings (name, phone, service, date, time, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, phone, service, date, time, notes))
        conn.commit()
        conn.close()

        msg = f"New Booking!%0AName: {name}%0APhone: {phone}%0AService: {service}%0ADate: {date}%0ATime: {time}%0ANotes: {notes}"
        whatsapp_url = f"https://wa.me/60168783226?text={msg}"

        flash("Booking submitted successfully!", "success")
        return redirect(whatsapp_url)

    from datetime import date as date_type
    today = date_type.today().isoformat()
    return render_template("book.html", today=today, form_data={})
    

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db()
        admin = conn.execute("SELECT * FROM admin WHERE username = ?", (username,)).fetchone()
        conn.close()
        if admin and check_password_hash(admin["password"], password):
          session["admin"] = True
          return redirect(url_for("admin_dashboard"))
        else:
          flash("Invalid credentials", "danger")
    
    return render_template("admin_login.html")
    

@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    
    conn = get_db()
    bookings = conn.execute("SELECT * FROM bookings ORDER BY date ASC, time ASC").fetchall()
    conn.close()
    return render_template("admin.html", bookings = bookings)


@app.route("/admin/update/<int:booking_id>", methods=["POST"])
def update_booking(booking_id):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    
    status = request.form.get("status")
    conn = get_db()
    conn.execute("UPDATE bookings SET status = ? WHERE id = ?", (status, booking_id))
    conn.commit()
    conn.close()
    flash("Booking updated successfully!", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/delete/<int:booking_id>", methods=["POST"])
def delete_booking(booking_id):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    
    conn = get_db()
    conn.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
    conn.commit()
    conn.close()
    flash("Booking deleted.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    flash("Logged out successfully!", "success")
    return redirect(url_for("admin_login"))

#run
if __name__ == "__main__":
    init_db()
    app.run(debug=True)