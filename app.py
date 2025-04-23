from flask import Flask, render_template, request, redirect, url_for, flash, session
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_bcrypt import Bcrypt
from flask_session import Session
import os
import random  # <-- for random price generation

# Flask App Setup
app = Flask(__name__)
app.secret_key = "your_secret_key"

# PostgreSQL Database Configuration
DB_CONFIG = {
    "dbname": "user_db",
    "user": "your_db_user",
    "password": "newpassword",  # Replace with your actual password
    "host": "localhost",
    "port": "5432"
}

# Initialize Bcrypt for Password Hashing
bcrypt = Bcrypt(app)

# Flask Session Configuration
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Function to Connect to PostgreSQL
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

# Function to Get Image Filenames
def get_image_filenames():
    image_folder = os.path.join(app.static_folder, 'images')
    image_filenames = os.listdir(image_folder)
    return image_filenames

# Route: Show Login/Register Page
@app.route("/")
def auth_page():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("authentication.html")

# Route: Handle User Registration
@app.route("/register", methods=["POST"])
def register():
    email = request.form["email"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    if password != confirm_password:
        flash("Passwords do not match!", "error")
        return redirect(url_for("auth_page"))

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cur.fetchone()
        if existing_user:
            flash("Email already registered!", "error")
            return redirect(url_for("auth_page"))

        cur.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_password))
        conn.commit()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for("auth_page"))

    except Exception as e:
        flash(f"Database error: {e}", "error")
        return redirect(url_for("auth_page"))

    finally:
        cur.close()
        conn.close()

# Route: Handle User Login
@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()

        if user and bcrypt.check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password!", "error")
            return redirect(url_for("auth_page"))

    except Exception as e:
        flash(f"Database error: {e}", "error")
        return redirect(url_for("auth_page"))

    finally:
        cur.close()
        conn.close()

# Route: Dashboard
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please log in first!", "error")
        return redirect(url_for("auth_page"))

    image_filenames = get_image_filenames()
    products = [{
        'id': i,
        'name': f'Product {i + 1}',
        'image': f'images/{filename}',
        'price': random.randint(70, 100)
    } for i, filename in enumerate(image_filenames)]

    return render_template("dashboard.html", products=products)

# Route: Logout
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Logged out successfully!", "success")
    return redirect(url_for("auth_page"))

# Run Flask App on Local Network
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

