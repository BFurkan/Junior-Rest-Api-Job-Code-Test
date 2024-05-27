from flask import request, jsonify
from app.models import Student, Grade
from app import app,db

@app.route('/api/students', methods=['POST'])  #Create students by their Name, Surname, Student Number and Grade
def create_student():
    data = request.json
    name = data.get('name')
    surname = data.get('surname')
    std_number = data.get('std_number')
    grades = data.get('grades')

    if not all([name, surname, std_number, grades]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        student = Student(name=name, surname=surname, std_number=std_number)
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
    
@app.route('/api/calculate-average/<std_number>', methods=['GET']) # GET for average calculation for multiple grades
def calculate_average(std_number):
    student = Student.query.filter_by(std_number=std_number).first()
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