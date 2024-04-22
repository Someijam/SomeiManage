from flask import Flask
from flask import jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy import text
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

# 查询部分
@app.route('/query/studentsinfo') # 学生信息
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

@app.route('/query/coursesinfo') # 课程信息
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

@app.route('/query/scoreinfo/<string:dept>/<string:cno>') # 成绩排名(专业系，课程号)
def scoreinfo(dept, cno):
    # SELECT Sno, Sname, Cno, Cname, Grade FROM CS_View WHERE Cno = '1' ORDER BY Grade DESC; # 排名
    # SELECT AVG(Grade) as Average_Grade FROM CS_View WHERE Cno = '1'; # 平均分
    # SELECT MAX(Grade) as Max_Grade FROM CS_View WHERE Cno = '1'; # 最高分
    # SELECT MIN(Grade) as Min_Grade FROM CS_View WHERE Cno = '1'; # 最低分
    # SELECT (SELECT COUNT(*) FROM CS_View WHERE Cno = '1' AND Grade >= 90) / (SELECT COUNT(*) FROM CS_View WHERE Cno = '1') as Excellent_Rate; # 优秀率
    # SELECT COUNT(*) as Fail_Count FROM CS_View WHERE Cno = '1' AND Grade < 60; # 不及格人数
    scoreStr=f'SELECT Sno, Sname, Cno, Cname, Grade FROM {dept}_View WHERE Cno = \'{cno}\' ORDER BY Grade DESC;'
    avgStr=f'SELECT AVG(Grade) as Average_Grade FROM {dept}_View WHERE Cno = \'{cno}\';'
    maxStr=f'SELECT MAX(Grade) as Max_Grade FROM {dept}_View WHERE Cno = \'{cno}\';'
    minStr=f'SELECT MIN(Grade) as Min_Grade FROM {dept}_View WHERE Cno = \'{cno}\';'
    excellentStr=f'SELECT (SELECT COUNT(*) FROM {dept}_View WHERE Cno = \'{cno}\' AND Grade >= 90) / (SELECT COUNT(*) FROM {dept}_View WHERE Cno = \'{cno}\') as Excellent_Rate;'
    failStr=f'SELECT COUNT(*) as Fail_Count FROM {dept}_View WHERE Cno = \'{cno}\' AND Grade < 60;'
    scoreSQL=text(scoreStr)
    avgSQL=text(avgStr)
    maxSQL=text(maxStr)
    minSQL=text(minStr)
    excellentSQL=text(excellentStr)
    failSQL=text(failStr)
    # print(scoreSQL)
    scores = db.session.execute(scoreSQL)
    scores_info = []
    for score in scores:
        score_dict = {
            "sno": score.Sno,
            "sname": score.Sname,
            "cno": score.Cno,
            "cname": score.Cname,
            "grade": score.Grade
        }
        scores_info.append(score_dict)
    avgVal = db.session.execute(avgSQL).fetchone()
    maxVal = db.session.execute(maxSQL).fetchone()
    minVal = db.session.execute(minSQL).fetchone()
    excellentVal = db.session.execute(excellentSQL).fetchone()
    excellentValPercent = round(100 * excellentVal[0],2)
    failVal = db.session.execute(failSQL).fetchone()
    return jsonify({'dept': dept,"cno":cno, 'dataarr': scores_info, 'average_grade': round(avgVal[0],2), 'max_grade': maxVal[0], 'min_grade': minVal[0], 'excellent_rate': excellentValPercent, 'fail_count': failVal[0]})

@app.route('/query/singlestuinfo/<string:sno>') # 单个学生个人信息
def singlestuinfo(sno):
    # SQL: SELECT Sno,Sname,Ssex,Sage,Sdept,Scholarship FROM Student WHERE Sno = 'sno';
    student = Student.query.filter(Student.Sno == sno).first()
    return jsonify({'dataname': 'singlestuinfo', 'sname': student.Sname, 'sno': student.Sno, 'ssex': student.Ssex, 'sage': student.Sage, 'sdept': student.Sdept, 'scholarship': student.Scholarship})

@app.route('/query/singlestuscore/<string:sno>') # 单个学生成绩信息
def singlestuscore(sno):
    # SQL:SELECT SC.Cno, Course.Cname, SC.Grade, Course.Ccredit FROM SC JOIN Course ON SC.Cno = Course.Cno WHERE SC.Sno = '200215121';
    stuscoreStr=f'SELECT SC.Cno, Course.Cname, SC.Grade, Course.Ccredit FROM SC JOIN Course ON SC.Cno = Course.Cno WHERE SC.Sno = \'{sno}\';'
    stuscoreSQL=text(stuscoreStr)
    stuscores = db.session.execute(stuscoreSQL)
    stuscores_info = []
    for stuscore in stuscores:
        stuscore_dict = {
            "cno": stuscore.Cno,
            "cname": stuscore.Cname,
            "grade": stuscore.Grade,
            "credit": stuscore.Ccredit
        }
        stuscores_info.append(stuscore_dict)
    return jsonify({'dataname': 'singlestuscore', 'dataarr': stuscores_info})

# 增加部分
@app.route('/add/studentinfo', methods=['POST']) # 添加新同学
def add_student():
    # SQL: INSERT INTO Student VALUES('202110000', '刘坤', '男', 22, 'CS', '否');
    data=request.get_json()
    # print(data)
    addstuStr=f"INSERT INTO Student VALUES('{data['add_s_no']}', '{data['add_s_name']}', '{data['add_s_sex']}', {data['add_s_age']}, '{data['add_s_dept']}', '{data['add_s_scholarship']}');"
    print(addstuStr)
    addstuSQL=text(addstuStr)
    db.session.execute(addstuSQL)
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/add/courseinfo', methods=['POST']) # 添加新课程
def add_course():
    # SQL: INSERT INTO Course VALUES('4', '操作系统', NULL,3);
    data=request.get_json()
    # print(data)
    addcourseStr=f"INSERT INTO Course VALUES('{data['add_c_no']}', '{data['add_c_name']}', '{data['add_c_pno']}', {data['add_credit']});"
    print(addcourseStr)
    addcourseSQL=text(addcourseStr)
    db.session.execute(addcourseSQL)
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/add/scorerecord', methods=['POST']) # 添加成绩
def add_score():
    # SQL: INSERT INTO SC VALUES('200215121', '2',85);
    data=request.get_json()
    # print(data)
    addscoreStr=f"INSERT INTO SC VALUES('{data['addscore_s_no']}', '{data['addscore_c_no']}', {data['addscore_sc']});"
    print(addscoreStr)
    addscoreSQL=text(addscoreStr)
    db.session.execute(addscoreSQL)
    db.session.commit()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    # db.create_all()  # 创建所有表
    app.run(port=5880, host='0.0.0.0')
