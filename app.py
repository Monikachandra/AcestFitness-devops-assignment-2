import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from datetime import datetime, date
import random
from fpdf import FPDF
import os

app = Flask(__name__)
app.secret_key = "aceest_secret_key"
DB_NAME = "aceest_fitness.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Users
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        role TEXT
    )
    """)
    
    # Clients
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        age INTEGER,
        height REAL,
        weight REAL,
        program TEXT,
        calories INTEGER,
        target_weight REAL,
        target_adherence INTEGER,
        membership_status TEXT,
        membership_end TEXT
    )
    """)
    
    # Progress
    cur.execute("""
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_name TEXT,
        week TEXT,
        adherence INTEGER
    )
    """)
    
    # Workouts
    cur.execute("""
    CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_name TEXT,
        date TEXT,
        workout_type TEXT,
        duration_min INTEGER,
        notes TEXT
    )
    """)
    
    # Exercises
    cur.execute("""
    CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        workout_id INTEGER,
        name TEXT,
        sets INTEGER,
        reps INTEGER,
        weight REAL
    )
    """)
    
    # Metrics
    cur.execute("""
    CREATE TABLE IF NOT EXISTS metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_name TEXT,
        date TEXT,
        weight REAL,
        waist REAL,
        bodyfat REAL
    )
    """)
    
    # Add default admin if not exists
    cur.execute("SELECT * FROM users WHERE username='admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO users VALUES ('admin','admin','Admin')")
    
    conn.commit()
    conn.close()

# Program templates for AI generator
PROGRAM_TEMPLATES = {
    "Fat Loss": ["Full Body HIIT", "Circuit Training", "Cardio + Weights"],
    "Muscle Gain": ["Push/Pull/Legs", "Upper/Lower Split", "Full Body Strength"],
    "Beginner": ["Full Body 3x/week", "Light Strength + Mobility"]
}

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)).fetchone()
        conn.close()
        
        if user:
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    clients = conn.execute("SELECT * FROM clients ORDER BY name").fetchall()
    conn.close()
    
    return render_template('dashboard.html', clients=clients)

@app.route('/client/add', methods=['POST'])
def add_client():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    name = request.form['name']
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO clients (name, membership_status) VALUES (?, ?)", (name, "Active"))
        conn.commit()
        flash(f"Client {name} added successfully")
    except sqlite3.IntegrityError:
        flash(f"Client {name} already exists")
    finally:
        conn.close()
    
    return redirect(url_for('dashboard'))

@app.route('/client/<int:client_id>')
def client_details(client_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    client = conn.execute("SELECT * FROM clients WHERE id=?", (client_id,)).fetchone()
    if not client:
        conn.close()
        flash("Client not found")
        return redirect(url_for('dashboard'))
    
    workouts = conn.execute("SELECT * FROM workouts WHERE client_name=? ORDER BY date DESC", (client['name'],)).fetchall()
    progress = conn.execute("SELECT * FROM progress WHERE client_name=? ORDER BY id", (client['name'],)).fetchall()
    metrics = conn.execute("SELECT * FROM metrics WHERE client_name=? ORDER BY date DESC", (client['name'],)).fetchall()
    conn.close()
    
    return render_template('client_details.html', client=client, workouts=workouts, progress=progress, metrics=metrics)

@app.route('/client/<int:client_id>/generate_program')
def generate_program(client_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    client = conn.execute("SELECT * FROM clients WHERE id=?", (client_id,)).fetchone()
    if not client:
        conn.close()
        return redirect(url_for('dashboard'))
    
    program_type = random.choice(list(PROGRAM_TEMPLATES.keys()))
    program_detail = random.choice(PROGRAM_TEMPLATES[program_type])
    
    conn.execute("UPDATE clients SET program=? WHERE id=?", (program_detail, client_id))
    conn.commit()
    conn.close()
    
    flash(f"Generated {program_type} program: {program_detail}")
    return redirect(url_for('client_details', client_id=client_id))

@app.route('/client/<int:client_id>/report')
def generate_report(client_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    client = conn.execute("SELECT * FROM clients WHERE id=?", (client_id,)).fetchone()
    conn.close()
    
    if not client:
        return redirect(url_for('dashboard'))
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"ACEest Client Report - {client['name']}", ln=True)
    pdf.set_font("Arial", "", 12)
    
    cols = ["ID", "Name", "Age", "Height", "Weight", "Program", "Calories", "Target Weight", "Target Adherence", "Membership", "End"]
    for col in cols:
        val = client[col.lower().replace(" ", "_")] if col.lower().replace(" ", "_") in client.keys() else "N/A"
        pdf.cell(0, 10, f"{col}: {val}", ln=True)
    
    report_path = f"/tmp/{client['name']}_report.pdf"
    pdf.output(report_path)
    
    return send_file(report_path, as_attachment=True)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
