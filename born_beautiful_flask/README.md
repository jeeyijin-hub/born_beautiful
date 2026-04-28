# Born Beautiful Beauty Centre

i build a full-stack web application for a beauty salon in Kuching, Sarawak, Malaysia. Built as the final project for CS50x 2026.

## Video Demo
https://youtu.be/hj8I4n0XEbw

## Description

Born Beautiful is a professional beauty salon website with an integrated online booking system and admin dashboard. The project solves a real-world problem for an actual client — helping a local beauty salon establish an online presence and streamline appointment bookings.

### Features

**Customer-facing:**
- Responsive beauty salon website with professional design
- Service menu with full pricing
- Online booking form with real-time validation
- WhatsApp integration for booking confirmation
- Social media links

**Admin Dashboard:**
- Secure login with hashed passwords
- View all bookings sorted by date
- Update booking status (pending/confirmed/cancelled)
- Delete bookings
- Direct WhatsApp link to each customer

### Technical Stack

- **Backend:** Python, Flask
- **Database:** SQLite, Postgres in Railway
- **Frontend:** HTML, CSS, JavaScript
- **Security:** Werkzeug password hashing
- **Deployment:** Railway
- **Performance:** 100/100 Lighthouse score (real environment)

### Design Decisions

**Why Flask?**
Flask was chosen for its simplicity and alignment with CS50x Week 9 content. It provides just enough structure for this project without unnecessary complexity.

**Why SQLite?**
This is a small business application with low concurrent users. SQLite is sufficient, lightweight, and requires no additional setup.

**Why hand-coded HTML/CSS instead of WordPress?**
Performance. WordPress-based beauty salon websites typically score 10-40 on Lighthouse Performance. This hand-coded site achieves 95+, resulting in faster load times and better Google rankings.

**Why WhatsApp integration?**
The salon owner already uses WhatsApp to communicate with clients. Integrating it reduces friction — clients book online, the owner gets notified via WhatsApp immediately.

### Security

- Admin passwords are hashed using Werkzeug's `generate_password_hash`
- Session management for admin authentication
- Input validation on booking form (past dates rejected, duplicate time slots detected)

## How to Run

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python app.py`
4. Visit `http://127.0.0.1:5000`

Admin login: `/admin/login`

## Files

- `app.py` — Main Flask application, routes, database functions
- `templates/` — HTML templates using Jinja2
- `static/` — CSS, JavaScript, images, fonts
- `database.db` — SQLite database