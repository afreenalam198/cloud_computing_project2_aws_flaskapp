import os
import sqlite3
import bcrypt  
from flask import Flask, g, request, render_template, redirect, url_for, session, send_file, flash
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management

DATABASE = '/var/www/html/flaskapp/users.db'
UPLOAD_FOLDER = '/var/www/html/flaskapp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure upload directory exists
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def connect_db():
    sql = sqlite3.connect(DATABASE)
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite3_db'):
        g.sqlite3_db = connect_db()
    return g.sqlite3_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite3_db'):
        g.sqlite3_db.close()

# Login Route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password', '').encode('utf-8')  # Convert to bytes

        db = get_db()
        cursor = db.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()

        if result and bcrypt.checkpw(password, result['password']):  # Compare hashed password
            session['user_id'] = result['id']  # Store user ID in session
            return redirect(url_for('user_profile'))
        else:
            flash("Invalid Username or Password", "error")  # Flash the error message
            return redirect(url_for('login')) 

    return render_template('login.html')

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db = get_db()

        username = request.form.get('username')
        password = request.form.get('password', '').encode('utf-8')  # Convert to bytes
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        address = request.form.get('address')
        file = request.files.get('file')  # Get uploaded file

        # Check if username already exists
        existing_user = db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
        if existing_user:
            flash("Username already taken", "error")
            return redirect(url_for('register'))

        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())  # Hash password

        file_path = None
        if file and file.filename.endswith('.txt'):
            filename = secure_filename(file.filename)
            timestamp = int(time.time())  # Unique timestamp to prevent overwriting files
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{timestamp}_{filename}")
            file.save(file_path)

        cursor = db.execute("""
            INSERT INTO users (username, password, first_name, last_name, email, address, file_path) 
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (username, hashed_password, first_name, last_name, email, address, file_path))
        db.commit()

        session['user_id'] = cursor.lastrowid  
        flash("Registration successful!", "success")
        return redirect(url_for('user_profile'))

    return render_template('register.html')

# User Profile Route
@app.route('/user_profile')
def user_profile():
    if 'user_id' not in session:
        flash("Please log in first.", "error")
        return redirect(url_for('login'))
    
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (session['user_id'],)).fetchone()

    if not user:
        return render_template('register.html', error="User not found. Please register first.")

    word_count = 0
    if user["file_path"]:
        try:
            with open(user["file_path"], "r", encoding="utf-8") as file:
                word_count = len(file.read().split())
        except Exception as e:
            flash(f"Could not read file: {str(e)}", "error")

    return render_template('user_profile.html', user=user, word_count=word_count)

# File Download Route
@app.route('/download')
def download():
    if 'user_id' not in session:
        flash("Please log in first.", "error")
        return redirect(url_for('login'))
    
    db = get_db()
    user = db.execute("SELECT file_path FROM users WHERE id = ?", (session['user_id'],)).fetchone()

    if user and user["file_path"] and os.path.exists(user["file_path"]):
        return send_file(user["file_path"], as_attachment=True)

    flash("No file available for download", "error")
    return redirect(url_for('user_profile'))

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

