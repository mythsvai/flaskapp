from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os  # Add this line to import the os module

app = Flask(__name__)

# SQLite setup - Using a function to get DB connection
def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'users.db')  # Absolute path to the DB
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Create table if it doesn't exist
with get_db_connection() as conn:
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (username TEXT, password TEXT, firstname TEXT, lastname TEXT, email TEXT)''')
    conn.commit()

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    # Getting form data
    username = request.form['username']
    password = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']

    try:
        # Insert the new user into the database
        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password, firstname, lastname, email) VALUES (?, ?, ?, ?, ?)",
                      (username, password, firstname, lastname, email))
            conn.commit()

        # Redirect to the user's profile page after successful registration
        return redirect(url_for('profile', username=username))
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return "An error occurred. Please try again later."

@app.route('/profile/<username>')
def profile(username):
    try:
        # Fetch user details from the database
        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username=?", (username,))
            user = c.fetchone()

        # Render the profile page if user is found
        if user:
            return render_template('profile.html', user=user)
        else:
            return "User not found", 404
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return "An error occurred. Please try again later."

if __name__ == '__main__':
    app.run(debug=True)


