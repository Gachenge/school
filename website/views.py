from flask import Blueprint
from flask import render_template
from flask_login import login_required
from flask_login import current_user
from flask import request
from flask import flash
from models.user import User
from models import storage
from flask import redirect
from flask import url_for
from models.student import Student
from models.teacher import Teacher
from models.subjects import Subject
from models.subject_grades import SubjectGrade
from flask import jsonify

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route("/teachers")
def teach():
    teachers = storage.all(Teacher).values()
    subjects = storage.all(Subject).values()
    return render_template("teachers.html", user=current_user,
                           teachers=teachers, subjects=subjects)

@views.route('/adteacher', methods=['GET', 'POST'])
def adteacher():
    if request.method == 'POST':
        details = {
            'name': request.form.get('fname') + ' ' + request.form.get('lname'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone')
        }
        if details['email'] in [teacher.email for teacher in storage.all(Teacher).values()]:
            flash("Email address already registered", category='error')
            return redirect(url_for('views.teach'))
        for key, value in details.items():
            if value is None or value == "":
                flash("{} must not be empty".format(key), category='error')
                return redirect(url_for('views.teach'))
            elif len(value) < 3:
                flash("{} entered is invalid".format(key), category='error')
                return redirect(url_for('views.teach'))
        if len(request.form.get('fname')) < 3:
            flash("{} should be a minimum 3 characters long".format(details['fname']), category='error')
            return redirect(url_for('views.teach'))
        elif len(request.form.get('lname')) < 3:
            flash("{} should be a minimum 3 characters long".format(details['lname']), category='error')
            return redirect(url_for('views.teach'))
        elif not details['phone'].isdigit() and len(details['phone'] != 10):
            flash("Enter a valid phone number", category='error')
            return redirect(url_for('views.teach'))
        else:
            teacher = Teacher(**details)
            storage.new(teacher)
            storage.save()
            flash("{} created".format(teacher.name), category='success')
            return redirect(url_for('views.teach'))
    return render_template("adteacher.html", user=current_user)

@views.route("/delteacher", methods=['GET', 'POST'])
def delteacher():
    if request.method == 'POST':
        teachers = storage.all(Teacher).values()
        name = request.form.get('fname') + ' ' + request.form.get('lname')
        teacher_id = request.form.get('teacher_id')
        user = None
        for teacher in teachers:
            if teacher.name == name and teacher.teacher_id == int(teacher_id):
                user = teacher
        if user == None:
            flash("Teacher not found", category='error')
        else:
            storage.delete(user)
            storage.save()
            flash("Teacher deleted", category='success')
            return redirect(url_for('views.teach'))
    return render_template("delteacher.html", user=current_user)

@views.route("/upteacher", methods=['GET', 'POST'])
def upteacher():
    if request.method == 'POST':
        details = {
            'name': request.form.get('fname')+' '+request.form.get('lname'),
            'teacher_id': request.form.get('teacher_id'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone')
        }
        teachers = storage.all(Teacher).values()
        new = None
        for teacher in teachers:
            if teacher.name == details['name'] and teacher.teacher_id == int(details['teacher_id']):
                new = teacher
        if new is None:
            flash("Ensure the teacher name and Id match to a valid teacher", category='error')
            return redirect(url_for('views.teach'))
        for key, value in details.items():
            if value is None or value == "":
                flash("{} cannot be null".format(key), category='error')
                return redirect(url_for('views.teach'))
            if key == 'phone' and len(value) == 10:
                setattr(new, key, value)
        flash("Teacher updated", category='succes')
        return redirect(url_for('views.teach'))
    return render_template('upteacher.html', user=current_user)

@views.route("/students")
def students():
    students = storage.all(Student).values()
    subjects = storage.all(Subject).values()
    subject_grade = storage.all(SubjectGrade).values()
    return render_template("students.html", user=current_user,
                           students=students, subjects=subjects,
                           subject_grade=subject_grade)

@views.route("/delstudent", methods=['GET', 'POST'])
def delstudent():
    if request.method == 'POST':
        students = storage.all(Student).values()
        name = request.form.get('fname')+' '+request.form.get('lname')
        student_id = request.form.get('student_id')
        new = None
        for student in students:
            if student.name == name and student.student_id == int(student_id):
                new = student
        if new is None:
            flash("Student not found. check yor details and try again", category='error')
            return redirect(url_for('views.students'))
        storage.delete(new)
        storage.save()
        flash("Student deleted", category='success')
        return redirect(url_for('views.students'))
    return render_template("delstudent.html", user=current_user)

@views.route("/adstudent", methods=['GET', 'POST'])
def adstudent():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        subject_name = request.form['subject_name']
        teacher_fname = request.form['teacher_fname']
        teacher_lname = request.form['teacher_lname']
        grade = request.form['grade']
        
        if len(fname) < 3:
            flash("Input a valid first name", category='error')
            return redirect(url_for('views.students'))
        elif len(lname) < 3:
            flash("Input a valid last name", category='error')
            return redirect(url_for('views.students'))
        
        teacher_name = f"{teacher_fname} {teacher_lname}"
        if teacher_name not in [teacher.name for teacher in storage.all(Teacher).values()]:
            flash("Input a valid teacher", category='error')
            return redirect(url_for('views.students'))
        
        subjects = storage.all(Subject).values()
        subject = next((subj for subj in subjects if subj.name == subject_name), None)
        if not subject:
            flash("Input a valid subject", category='error')
            return redirect(url_for('views.students'))
        
        student = Student(name=f"{fname} {lname}")
        storage.new(student)
        
        grade = SubjectGrade(grade=grade)
        grade.subject_id = subject.subject_id
        grade.student_id = student.student_id
        storage.new(grade)
        
        subject.students.append(student)
        storage.save()
        
        flash("New student added", category='success')
        return redirect(url_for('views.students'))
    
    return render_template("adstudent.html", user=current_user)


@views.route("/upstudent", methods=['GET', 'POST'])
def upstudent():
    if request.method == 'POST':
        details = {
            'name': request.form.get('fname')+' '+request.form.get('lname'),
            'student_id': request.form.get('student_id'),
            'subject_name': request.form.get('subject_name'),
            'teacher_name': request.form.get('teacher_name'),
            'grade': request.form.get('grade')
        }
        new = None
        students = storage.all(Student).values()
        for student in students:
            if student.name == details['name'] and student.student_id == int(details['student_id']):
                new = student
        if not new:
            flash("Ensure you entered the correct name and id", category='error')
            return redirect(url_for('views.students'))
        for key, value in details.items():
            setattr(new, key, value)
        flash("Student updated", category='success')
        return redirect(url_for('views.students'))
    return render_template("upstudents.html", user=current_user)

@views.route("/subjects")
def subjects():
    subjects = storage.all(Subject).values()
    return render_template("subjects.html", user=current_user, subjects=subjects)
