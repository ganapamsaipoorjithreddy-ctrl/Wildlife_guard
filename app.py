from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Create database automatically
def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        location TEXT,
        description TEXT
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

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO reports (name, location, description) VALUES (?, ?, ?)",
                    (name, location, description))
        conn.commit()
        conn.close()

        return render_template('success.html')

    return render_template('report.html')

if __name__ == '__main__':
    app.run(debug=True)
