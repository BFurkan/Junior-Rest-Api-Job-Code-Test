from app import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    std_number = db.Column(db.String(20), nullable=False, unique=True)

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_code = db.Column(db.String(10), nullable=False)
    value = db.Column(db.Integer, nullable=False)

    student = db.relationship('Student', backref=db.backref('grades', lazy=True))
