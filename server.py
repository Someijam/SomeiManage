from flask import Flask
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://testserver:123456@localhost:13306/S_T_U202112643'
app.config['SQLALCHEMY_ECHO'] = True
app.json.ensure_ascii = False
db = SQLAlchemy(app)

class Student(db.Model):  # 定义一个 Student 模型
    __tablename__ = 'Student'
    Sno = db.Column(db.String(9), primary_key=True)
    Sname = db.Column(db.String(20))
    Ssex = db.Column(db.String(2))
    Sage = db.Column(db.Integer)
    Sdept = db.Column(db.String(20))
    Scholarship = db.Column(db.String(2))

class Course(db.Model):  # 定义一个 Course 模型
    __tablename__ = 'Course'
    Cno = db.Column(db.String(4), primary_key=True)
    Cname = db.Column(db.String(40))
    Cpno = db.Column(db.String(4))
    Ccredit = db.Column(db.Integer)

class SC(db.Model):  # 定义一个 SC 模型
    __tablename__ = 'SC'
    Sno = db.Column(db.String, primary_key=True)
    Cno = db.Column(db.String, primary_key=True)
    Grade = db.Column(db.Integer)

@app.route('/query/studentsinfo')
def studentsinfo():
    # SQL: SELECT Sno,Sname,Ssex,Sage,Sdept,Scholarship FROM Student;
    students = Student.query.all()  # 查询所有学生
    students_info = []
    for student in students:
        student_dict = {
            "key": student.Sno,
            "name": student.Sname,
            "sex": student.Ssex,
            "age": student.Sage,
            "dept": student.Sdept,
            "scholarship": student.Scholarship
        }
        students_info.append(student_dict)
    return jsonify({'dataname': 'studentsinfo', 'dataarr': students_info})

@app.route('/query/coursesinfo')
def coursesinfo():
    # SQL: SELECT Cno,Cname,Cpno,Ccredit FROM Course;
    # SQL: SELECT COUNT(DISTINCT Sno) as Student_Count FROM SC WHERE Cno = '1';
    courses = Course.query.all()
    courses_info = []
    for course in courses:
        student_count = db.session.query(func.count(SC.Sno)).filter(SC.Cno == course.Cno).scalar()
        course_dict = {
            "key": course.Cno,
            "name": course.Cname,
            "pno": course.Cpno,
            "credit": course.Ccredit,
            "student_count": student_count
        }
        courses_info.append(course_dict)
    return jsonify({'dataname': 'coursesinfo', 'dataarr': courses_info})

if __name__ == '__main__':
    # db.create_all()  # 创建所有表
    app.run(port=5880, host='0.0.0.0')