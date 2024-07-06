from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__, static_url_path='/static')

# Path to SQLite database file
DB_FILE = 'portfolio\contact_messages.db'

# Initialize SQLite database connection
def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# Create the table if it doesn't exist
def create_table():
    conn = get_db_connection()
    with conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contact_message (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL
            )
        ''')
    conn.close()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/education')
def education():
    return render_template('education.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit_contact_form', methods=['POST'])
def submit_contact_form():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Insert the form data into the database
        conn = get_db_connection()
        with conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO contact_message (name, email, message)
                VALUES (?, ?, ?)
            ''', (name, email, message))

        return render_template('contact_success.html', name=name)

    return 'Method Not Allowed', 405

@app.route('/view_messages')
def view_messages():
    conn = get_db_connection()
    messages = []
    with conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM contact_message')
        messages = cursor.fetchall()
    return render_template('view_messages.html', messages=messages)

if __name__ == '__main__':
    # Create the table if it doesn't exist
    create_table()

    app.run(debug=True)
