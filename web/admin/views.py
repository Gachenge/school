from web.admin.forms import (RegistrationForm, UserUpdateForm, TeacherRegistrationForm, StudentUpdateForm,
                              TeacherUpdateForm, StudentRegistrationForm, SubjectRegistrationForm)
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from web.models import User, Teacher, Subject, Student, SubjectGrade
from web import bcrypt, db

admin = Blueprint('admin', __name__)

@admin.route("/administrator")
@login_required
def administrator():
    return render_template("admin.html", title="Admin page")


@admin.route("/users", methods=['GET', 'POST'])
@login_required
def users():
    if current_user.role == 'admin':
        users = User.query.all()
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed, role=form.role.data)
            db.session.add(user)
            db.session.commit()
            flash("New user created", 'success')
            return redirect(url_for('admin.users'))
        return render_template("users.html", title='Users', users=users, form=form)
    else:
        flash("You do not have enough permissions to view this page", 'danger')
        return redirect(url_for('main.home'))

@admin.route("/user/<int:user_id>", methods=['GET', 'POST'])
def user_details(user_id):
    if current_user.role == 'admin':
        user_id = request.view_args['user_id']
        user = User.query.get_or_404(user_id)
        form = UserUpdateForm()
        if form.validate_on_submit():
            user.username = form.username.data
            user.email = form.email.data
            user.role = form.role.data
            db.session.commit()
            flash('User updated', 'success')
            return redirect(url_for('admin.users'))
        elif request.method == 'GET':
            form.username.data = user.username
            form.email.data = user.email
            form.role.data = user.role
        return render_template("user_details.html", form=form, user=user)
    else:
        flash("You do not have enough permissions to view this page", 'danger')
        return redirect(url_for('main.home'))

@admin.route("/user/<int:user_id>/delete")
def user_delete(user_id):
    if current_user.role == 'admin':
        user_id = request.view_args['user_id']
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash("User deleted", 'success')
        return redirect(url_for('admin.users'))
    else:
        flash("You do not have enough permissions to view this page", 'danger')
        return redirect(url_for('main.home'))
    
@admin.route("/teachers", methods=['GET', 'POST'])
@login_required
def teachers():
    if current_user.role == 'admin':
        teachers = Teacher.query.all()
        subjects = Subject.query.all()
        form = TeacherRegistrationForm()
        if form.validate_on_submit():
            teacher = Teacher(name=form.fname.data+' '+form.lname.data, email=form.email.data, phone=form.phone.data)
            db.session.add(teacher)
            db.session.commit()
            subject = Subject.query.filter_by(name=form.subject.data).first()
            if not subject:
                new = Subject(name=form.subject.data, teacher_id=teacher.id)
                db.session.add(new)
                db.session.commit()
                new.teacher.append(teacher)
                flash("Created new subject", 'success')
            else:
                subject.teacher.append(teacher)
                subject.teacher_id = teacher.id
            db.session.commit()
            return redirect(url_for('admin.teachers'))
        return render_template("teachers.html", form=form, teachers=teachers, subjects=subjects)
    else:
        flash("You do not have enough permissions to view this page", 'danger')
        return redirect(url_for('main.home'))
    
@admin.route("/teacher/<int:teacher_id>", methods=['GET', 'POST'])
def teacher_details(teacher_id):
    if current_user.role == 'admin':
        teacher_id = request.view_args['teacher_id']
        teacher = Teacher.query.get_or_404(teacher_id)
        form = TeacherUpdateForm()
        if form.validate_on_submit():
            teacher.name = form.fname.data + ' ' + form.lname.data
            teacher.email = form.email.data
            teacher.phone = form.phone.data
            subject_name = form.subject.data
            subject = Subject.query.filter_by(name=subject_name).first()
            if subject:
                subject.teacher.append(teacher)
            else:
                sub = Subject(name=subject_name, teacher_id=teacher.id)
                db.session.add(sub)
                sub.teacher.append(teacher)
            db.session.commit()
            flash('Teacher updated', 'success')
            return redirect(url_for('admin.teachers'))
        elif request.method == 'GET':
            form.fname.data, form.lname.data = teacher.name.split(" ")
            form.email.data = teacher.email
            form.phone.data = teacher.phone
        return render_template("teacher_details.html", form=form, teacher=teacher)
    else:
        flash("You do not have enough permissions to view this page", 'danger')
        return redirect(url_for('main.home'))

    
@admin.route("/teacher/<int:teacher_id>/delete")
def teacher_delete(teacher_id):
    if current_user.role == 'admin':
        teacher_id = request.view_args['teacher_id']
        teacher = Teacher.query.get_or_404(teacher_id)
        db.session.delete(teacher)
        db.session.commit()
        flash("Teacher deleted", 'success')
        return redirect(url_for('admin.teachers'))
    else:
        flash("You do not have enough permissions to view this page", 'danger')
        return redirect(url_for('main.home'))
    
@admin.route("/students", methods=['GET', 'POST'])
@login_required
def students():
    if current_user.role == 'admin':
        grades = SubjectGrade.query.all()
        students = Student.query.all()
        subjects = Subject.query.all()
        form = StudentRegistrationForm()
        if form.validate_on_submit():
            student = Student(name=form.fname.data+' '+form.lname.data)
            db.session.add(student)
            db.session.commit()
            subject = Subject.query.filter_by(name=form.subject.data).first()
            if not subject:
                new = Subject(name=form.subject.data, student_id=student.id)
                db.session.add(new)
                db.session.commit()
                new.student.append(student)
                grad = SubjectGrade(subject_id=new.id, student_id=student.id, grade=form.grade.data)
                db.session.add(grad)
                flash("Created new student", 'success')
            else:
                subject.student.append(student)
                subject.student_id = student.id
                grad = SubjectGrade(subject_id=subject.id, student_id=student.id, grade=form.grade.data)
                db.session.add(grad)
            db.session.commit()
            return redirect(url_for('admin.students'))
        return render_template("students.html", form=form, students=students, subjects=subjects, grades=grades)
    else:
        flash("You do not have enough permissions to view this page", 'danger')
        return redirect(url_for('main.home'))
    
@admin.route("/student/<int:student_id>", methods=['GET', 'POST'])
def student_details(student_id):
    if current_user.role == 'admin':
        student_id = request.view_args['student_id']
        student = Student.query.get_or_404(student_id)
        form = StudentUpdateForm()
        if form.validate_on_submit():
            student.name = form.fname.data + ' ' + form.lname.data
            student.subject = form.subject.data
            student.grade = form.grade.data
            subject_name = form.subject.data
            subject = Subject.query.filter_by(name=subject_name).first()
            if subject:
                subject.student.append(student)
            else:
                sub = Subject(name=subject_name, student_id=student.id)
                db.session.add(sub)
                sub.student.append(student)
            db.session.commit()
            grad = SubjectGrade(grade=form.grade.data, subject_id=subject.id, student_id=student.id)
            db.session.add(grad)
            db.session.commit()
            flash('student updated', 'success')
            return redirect(url_for('admin.students'))
        elif request.method == 'GET':
            form.fname.data, form.lname.data = student.name.split(" ")
        return render_template("student_details.html", form=form, student=student)
    else:
        flash("You do not have enough permissions to view this page", 'danger')
        return redirect(url_for('main.home'))
    
@admin.route("/student/<int:student_id>/delete")
def student_delete(student_id):
    if current_user.role == 'admin':
        student_id = request.view_args['student_id']
        student = Student.query.get_or_404(student_id)
        db.session.delete(student)
        db.session.commit()
        flash("Student deleted", 'success')
        return redirect(url_for('admin.students'))
    else:
        flash("You do not have enough permissions to view this page", 'danger')
        return redirect(url_for('main.home'))
    
@admin.route("/subjects", methods=['GET', 'POST'])
@login_required
def subjects():
    if current_user.role == 'admin':
        subjects = Subject.query.all()
        teachers = Teacher.query.all()
        students = Student.query.all()
        form = SubjectRegistrationForm()
        if form.validate_on_submit():
            subject = Subject.query.filter_by(name=form.subject.data).first()
            student = Student.query.filter_by(name=form.sfname.data+' '+form.slname.data).first()
            teacher = Teacher.query.filter_by(name=form.tfname.data+' '+form.tlname.data).first()
            if subject:
                flash("Subject already registered")
            else:
                subject = Subject(name=form.subject.data, student_id=student.id, teacher_id=teacher.id)
                db.session.add(subject)
                db.session.commit()
                teacher.subjects.append(subject)
                student.subjects.append(subject)
                if form.grade.data:
                    grad = SubjectGrade(grade=form.grade.data, student_id=student.id, subject_id=subject.id)
                    db.session.add(grad)
                db.session.commit()
                flash("New subject added", 'success')
            return redirect(url_for('admin.subjects'))
        return render_template("subjects.html", form=form, subjects=subjects, teachers=teachers, students=students)
    else:
        flash("You do not have enough permissions to view this page", 'danger')
        return redirect(url_for('main.home'))


@admin.route("/subject/<int:subject_id>", methods=['GET', 'POST'])
def subject_details(subject_id):
    if current_user.role == 'admin':
        subject_id = request.view_args['subject_id']
        subject = Subject.query.get_or_404(subject_id)
        form = SubjectRegistrationForm()
        if form.validate_on_submit():
            teacher = Teacher.query.filter_by(name=form.tfname.data + ' ' + form.tlname.data).first()
            student = Student.query.filter_by(name=form.sfname.data + ' ' + form.slname.data).first()
            if teacher is None:
                form.tfname.errors.append('Teacher not registered')
                return render_template("subject_details.html", form=form, subject=subject)
            if student is None:
                form.sfname.errors.append('Student not registered')
                return render_template("subject_details.html", form=form, subject=subject)
            subject.name = form.name.data
            subject.teacher_id = teacher.id
            subject.student_id = student.id

            teacher.subjects.append(subject)
            student.subjects.append(subject)
            subject.student.append(student)
            subject.teacher.append(teacher)
            
            flash("Subject updated", 'success')
            db.session.commit()
            return redirect(url_for('admin.subjects'))
        elif request.method == 'GET':
            form.name.data = subject.name
            teacher = Teacher.query.get(subject.teacher_id)
            student = Student.query.get(subject.student_id)

            if teacher:
                teacher_name_parts = teacher.name.split(' ')
                if len(teacher_name_parts) == 2:
                    form.tfname.data, form.tlname.data = teacher_name_parts

            if student:
                student_name_parts = student.name.split(' ')
                if len(student_name_parts) == 2:
                    form.sfname.data, form.slname.data = student_name_parts

        return render_template("subject_details.html", form=form, subject=subject)
    else:
        flash("You do not have enough permissions to view this page", 'danger')
        return redirect(url_for('main.home'))

    
@admin.route("/subject/<int:subject_id>/delete")
def subject_delete(subject_id):
    if current_user.role == 'admin':
        subject_id = request.view_args['subject_id']
        subject = Subject.query.get_or_404(subject_id)
        db.session.delete(subject)
        db.session.commit()
        flash("subject deleted", 'success')
        return redirect(url_for('admin.subjects'))
    else:
        flash("You do not have enough permissions to view this page", 'danger')
        return redirect(url_for('main.home'))
