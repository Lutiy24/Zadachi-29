from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                emp_id TEXT PRIMARY KEY,
                name TEXT,
                byear INTEGER,
                salary_per_hour REAL
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS timesheets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                emp_id TEXT,
                month TEXT,
                worked_hours REAL,
                FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        emp_id = request.form['emp_id']
        name = request.form['name']
        byear = request.form['byear']
        salary = request.form['salary']
        with sqlite3.connect("database.db") as conn:
            c = conn.cursor()
            c.execute('INSERT INTO employees VALUES (?, ?, ?, ?)',
                      (emp_id, name, byear, salary))
            conn.commit()
        return redirect('/')
    return render_template('add_employee.html')

@app.route('/add_timesheet', methods=['GET', 'POST'])
def add_timesheet():
    if request.method == 'POST':
        emp_id = request.form['emp_id']
        month = request.form['month']
        hours = request.form['hours']
        with sqlite3.connect("database.db") as conn:
            c = conn.cursor()
            c.execute('INSERT INTO timesheets (emp_id, month, worked_hours) VALUES (?, ?, ?)',
                      (emp_id, month, hours))
            conn.commit()
        return redirect('/')
    return render_template('add_timesheet.html')

@app.route('/top3')
def top3():
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute('''
            SELECT e.emp_id, e.name, SUM(t.worked_hours * e.salary_per_hour) AS total_salary
            FROM employees e
            JOIN timesheets t ON e.emp_id = t.emp_id
            GROUP BY e.emp_id
            ORDER BY total_salary DESC
            LIMIT 3
        ''')
        data = c.fetchall()
    return render_template('top3.html', employees=data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)