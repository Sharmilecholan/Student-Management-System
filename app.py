from flask import Flask, render_template, request, redirect, url_for
from db_connection import get_db_connection

app = Flask(__name__)

@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) AS total_students FROM Students")
    total_students = cursor.fetchone()['total_students']

    cursor.execute("SELECT COUNT(*) AS total_courses FROM Courses")
    total_courses = cursor.fetchone()['total_courses']

    conn.close()
    return render_template('dashboard.html', total_students=total_students, total_courses=total_courses)

@app.route('/students')
def student_list():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Students")
    students = cursor.fetchall()
    conn.close()
    return render_template('student_list.html', students=students)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        email = request.form['email']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Students (first_name, last_name, dob, email) VALUES (%s, %s, %s, %s)",
                       (first_name, last_name, dob, email))
        conn.commit()
        conn.close()
        return redirect(url_for('student_list'))
    return render_template('add_student.html')

@app.route('/courses')
def course_management():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Courses")
    courses = cursor.fetchall()
    conn.close()
    return render_template('course_management.html', courses=courses)

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        course_name = request.form['course_name']
        credits = request.form['credits']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Courses ( course_name, credits) VALUES ( %s, %s)",
                       ( course_name, credits))
        conn.commit()
        conn.close()
        return redirect(url_for('course_management'))
    return render_template('add_course.html')

if __name__ == '__main__':
    app.run(debug=True)
