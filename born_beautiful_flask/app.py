from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_compress import Compress
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date as date_type, datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-key-only")

# database
database_url = os.environ.get("DATABASE_URL", "sqlite:///database.db")
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
Compress(app)

# MODELS
class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    service = db.Column(db.Text, nullable=False)
    date = db.Column(db.Text, nullable=False)
    time = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text)
    status = db.Column(db.Text, default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)


with app.app_context():
    db.create_all()
    admin_password = os.environ.get("ADMIN_PASSWORD", "bornbeautiful2026")
    existing = Admin.query.filter_by(username="admin").first()
    if not existing:
        admin = Admin(
            username="admin",
            password=generate_password_hash(admin_password)
        )
        db.session.add(admin)
        db.session.commit()
    else:
        existing.password = generate_password_hash(admin_password)
        db.session.commit()

# ROUTES
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/book", methods=["GET", "POST"])
def book():
    from datetime import date as date_type, datetime
    today = date_type.today().isoformat()

    if request.method == "POST":
        name    = request.form.get("name")
        phone   = request.form.get("phone")
        service = request.form.get("service")
        date    = request.form.get("date")
        time    = request.form.get("time")
        notes   = request.form.get("notes")

        now = datetime.now()

        if date < today:
            flash("Please select a future date.", "danger")
            return render_template("book.html", today=today, form_data=request.form)

        if date == today:
            time_map = {
                "9:00 AM": 9, "10:00 AM": 10, "11:00 AM": 11,
                "12:00 PM": 12, "1:00 PM": 13, "2:00 PM": 14,
                "3:00 PM": 15, "4:00 PM": 16, "5:00 PM": 17
            }
            selected_hour = time_map.get(time, 0)
            if selected_hour <= now.hour:
                flash("This time slot has already passed. Please select a future time.", "danger")
                return render_template("book.html", today=today, form_data=request.form)

        existing = Booking.query.filter_by(date=date, time=time).filter(
            Booking.status != "cancelled"
        ).first()

        if existing:
            flash("This time slot is already booked. Please choose a different time.", "danger")
            return render_template("book.html", today=today, form_data=request.form)

        booking = Booking(
            name=name, phone=phone, service=service,
            date=date, time=time, notes=notes
        )
        db.session.add(booking)
        db.session.commit()

        msg = f"New Booking!%0AName: {name}%0APhone: {phone}%0AService: {service}%0ADate: {date}%0ATime: {time}%0ANotes: {notes}"
        whatsapp_url = f"https://wa.me/60168783226?text={msg}"
        return redirect(whatsapp_url)

    return render_template("book.html", today=today, form_data={})

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password_hash(admin.password, password):
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid credentials", "danger")

    return render_template("admin_login.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    bookings = Booking.query.order_by(Booking.date.asc(), Booking.time.asc()).all()
    return render_template("admin.html", bookings=bookings)

@app.route("/admin/update/<int:booking_id>", methods=["POST"])
def update_booking(booking_id):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    booking = Booking.query.get_or_404(booking_id)
    booking.status = request.form.get("status")
    db.session.commit()
    flash("Booking updated successfully!", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/delete/<int:booking_id>", methods=["POST"])
def delete_booking(booking_id):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    flash("Booking deleted.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))

@app.route("/sitemap.xml")
def sitemap():
    from flask import send_from_directory
    return send_from_directory(".", "sitemap.xml")

if __name__ == "__main__":
    app.run(debug=True)