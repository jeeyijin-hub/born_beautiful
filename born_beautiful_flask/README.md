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

## Challenges

Building this project came with several challenges that helped me grow as a developer.

The first major challenge was deploying Flask to Railway. Unlike static sites on Netlify, Flask requires a production WSGI server. I had to learn how to configure Gunicorn, set up a Procfile, and manage environment variables for security — keeping sensitive data like passwords and secret keys out of the GitHub repository.

The second challenge was database migration. I initially used SQLite for development, but discovered that SQLite files are lost on every Railway redeployment. This would have caused all customer booking data to disappear every time I updated the code. I solved this by migrating to PostgreSQL using Flask-SQLAlchemy, which also taught me how to write database-agnostic code that works with both SQLite locally and PostgreSQL in production.

The third challenge was Lighthouse performance optimization. Early versions of the site scored 85-87 on Performance due to Google Fonts blocking the page render. I solved this by self-hosting the fonts locally, which eliminated the external network request and brought the score up to 100.

## Future Improvements

- Add email notifications for booking confirmations
- Add a calendar view in the admin dashboard to visualize bookings
- Add Google Maps embed in the contact section
- Support multiple staff members with individual schedules
- Add a promotions page that the salon owner can update from the admin dashboard
- Implement Google Analytics to track website visitors and booking conversion rates

## Acknowledgements

Built as the CS50x 2026 final project by Jee Yi Jin from Kuching, Sarawak, Malaysia. Special thanks to the CS50 team at Harvard University for providing an excellent introduction to computer science.