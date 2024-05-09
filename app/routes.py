from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import Student, Grade

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/api/students', methods=['POST'])  #Create students by their Name, Surname, Student Number and Grade
def create_student():
    data = request.json
    name = data.get('name')
    surname = data.get('surname')
    stdNumber = data.get('stdNumber')
    grades = data.get('grades')

    if not all([name, surname, stdNumber, grades]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        student = Student(name=name, surname=surname, stdNumber=stdNumber)
        db.session.add(student)
        db.session.commit()

        for grade_data in grades:
            course_code = grade_data.get('code')
            value = grade_data.get('value')
            if course_code and value:
                grade = Grade(student_id=student.id, course_code=course_code, value=value)
                db.session.add(grade)

        db.session.commit()

        return jsonify({'message': 'Student created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/calculate-average/<stdNumber>', methods=['GET']) # GET for average calculation for multiple grades
def calculate_average(stdNumber):
    student = Student.query.filter_by(stdNumber=stdNumber).first()
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    grades = Grade.query.filter_by(student_id=student.id).all()
    if not grades:
        return jsonify({'message': 'No grades found for this student'})
    
    average_grades = {}
    for grade in grades:
        if grade.course_code not in average_grades:
            average_grades[grade.course_code] = [grade.value]
        else:
            average_grades[grade.course_code].append(grade.value)

    for course_code, values in average_grades.items():
        average_grades[course_code] = round(sum(values) / len(values), 2)

    return jsonify(average_grades), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
