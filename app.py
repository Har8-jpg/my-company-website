from flask import Flask, render_template, request, redirect, session
import sqlite3
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "secret123"
bcrypt = Bcrypt(app)

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ---------------- HOME ----------------
@app.route('/')
def home():
    return redirect('/login')

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                      (username, hashed_password))
            conn.commit()
        except:
            return "User already exists"

        conn.close()
        return redirect('/login')

    return render_template('register.html')

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        c.execute("SELECT password FROM users WHERE username = ?", (username,))
        user = c.fetchone()

        conn.close()

        if user and bcrypt.check_password_hash(user[0], password):
            session['user'] = username
            return redirect('/dashboard')
        else:
            return "Invalid credentials"

    return render_template('login.html')

# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    return render_template('dashboard.html', user=session['user'])

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)
