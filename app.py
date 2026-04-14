from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Create database
def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        location TEXT,
        description TEXT,
        image TEXT,
        latitude TEXT,
        longitude TEXT
    )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        description = request.form['description']
        latitude = request.form['latitude']
        longitude = request.form['longitude']

        image = request.files['image']
        filename = image.filename
        if filename != "":
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO reports (name, location, description, image, latitude, longitude)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (name, location, description, filename, latitude, longitude))

        conn.commit()
        conn.close()

        return redirect('/success')

    return render_template('report.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/admin')
def admin():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM reports")
    data = cur.fetchall()
    conn.close()

    return render_template('admin.html', reports=data)

if __name__ == '__main__':
    app.run(debug=True)
