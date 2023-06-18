from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user
from web.models import SubjectGrade, Subject, Student
from web.student.forms import StudentAccountForm
from web import db

student = Blueprint('student', __name__)

@student.route("/student_account", methods=['GET', 'POST'])
@login_required
def student_account():
    if current_user.role == 'student':
        grades = SubjectGrade.query.all()
        subjects = Subject.query.all()
        form = StudentAccountForm()
        if form.validate_on_submit():
            current_user.name = form.fname.data+' '+form.lname.data
            current_user.email = form.email.data
            current_user.username = form.username.data
            db.session.commit()
            flash("Records updated", 'success')
        elif request.method == 'GET':
            if current_user.name:
                form.fname.data, form.lname.data = current_user.name.split(' ')
            form.email.data = current_user.email
            form.username.data = current_user.username
        student = Student.query.filter_by(email=current_user.email).first()
        return render_template("studentAccount.html", form=form, student=student, grades=grades, subjects=subjects)
    else:
        flash("You do not have sufficient permissions to view this page", 'danger')
        return redirect(url_for('main.home'))
