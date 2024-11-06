from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)

# Database connection configuration
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',           # Your database username
        password='',   # Your database password
        database='employee_crud'  # Your database name
    )

# Home route - Display all employees
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM employees')
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', employees=employees)

# Create employee route
@app.route('/create', methods=['GET', 'POST'])
def create_employee():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        position = request.form['position']
        salary = request.form['salary']

        if not name and not email and not position and not salary:
            return 'Name, Email, Position, and Salary are required', 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO employees (name, email, position, salary) VALUES (%s, %s, %s, %s)', (name, email, position, salary))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create_employee.html')

# Update employee route
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_employee(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM employees WHERE id = %s', (id,))
    employee = cursor.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        position = request.form['position']
        salary = request.form['salary']

        if not name and not email and not position and not salary:
            return 'Name, Email, Position, and Salary are required', 400

        cursor.execute('UPDATE employees SET name = %s, email = %s, position = %s, salary = %s WHERE id = %s', (name, email, position, salary, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))

    cursor.close()
    conn.close()
    return render_template('update_employee.html', employee=employee)

# Delete employee route
@app.route('/delete/<int:id>', methods=['GET'])
def delete_employee(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM employees WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
