from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user
from web.models import Teacher, Subject, Student, SubjectGrade, subject_teacher_association, subject_student_association
from web.teacher.forms import TeacherAccountForm
from web import db

teacher = Blueprint('teacher', __name__)

@teacher.route("/teacher_account", methods=['GET', 'POST'])
@login_required
def teacher_account():
    if current_user.role == 'teacher':
        form = TeacherAccountForm()
        if form.validate_on_submit():
            current_user.name = form.name.data
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.phone = form.phone.data
            db.session.commit()
            flash("Records updated", 'success')
        elif request.method == 'GET':
            if current_user.name:
                form.name.data = current_user.name
            form.username.data = current_user.username
            form.email.data = current_user.email
            form.phone.data = current_user.phone
        teacher = Teacher.query.filter_by(email=current_user.email).first()
        return render_template("teacherAccount.html", form=form)
    else:
        flash("You do not have sufficient permissions to view this page", 'danger')      

@teacher.route("/teacher_account/students", methods=['GET', 'POST'])
@login_required
def studentScores():
    if current_user.role == 'teacher':
        teacher = Teacher.query.filter_by(email=current_user.email).first()
        subjects = Subject.query.join(subject_teacher_association).filter_by(teacher_id=teacher.id).all()
        if request.method == 'POST':
            for key, value in request.form.items():
                if key.startswith("score_"):
                    _, subject_id, student_id = key.split("_")
                    subject_id = int(subject_id)
                    student_id = int(student_id)
                    score = int(value) if value else None  # Convert to int if not empty, otherwise None

                    existing_grade = SubjectGrade.query.filter_by(subject_id=subject_id, student_id=student_id).first()

                    if score is not None:
                        if existing_grade:
                            existing_grade.grade = score
                        else:
                            new_grade = SubjectGrade(subject_id=subject_id, student_id=student_id, grade=score)
                            db.session.add(new_grade)

            db.session.commit()
            flash("Scores saved successfully", 'success')
            return redirect(url_for('teacher.studentScores'))
        subjects_dict = {}
        for subject in subjects:
            students = Student.query.join(subject_student_association).filter_by(subject_id=subject.id).all()
            subjects_dict[subject.id] = students
        grades = SubjectGrade.query.all()
        return render_template("teacherSubjects.html", subjects_dict=subjects_dict, subjects=subjects, grades=grades)
    else:
        flash("You do not have sufficient permissions to view this page", 'danger')
        return redirect(url_for('main.home'))
