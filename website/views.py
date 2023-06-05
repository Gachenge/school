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
from models.blog import Blog
from website.forms import PostForm
from flask import abort

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
@login_required
def home():
    posts = storage.all(Blog).values()
    return render_template("home.html", user=current_user, posts=posts)

@views.route("/teachers")
def teachers():
    teachers = storage.all(Teacher).values()
    subjects = storage.all(Subject).values()
    return render_template("teachers.html", user=current_user, teachers=teachers,
                           subjects=subjects)

@views.route("/students")
def students():
    students = storage.all(Student).values()
    subjects = storage.all(Subject).values()
    grades = storage.all(SubjectGrade).values()
    return render_template("students.html", user=current_user, students=students,
                           subjects=subjects, grades=grades)

@views.route("/subjects")
def subjects():
    students = storage.all(Student).values()
    teachers = storage.all(Teacher).values()
    subjects = storage.all(Subject).values()
    return render_template("subjects.html", user=current_user, students=students,
                           teachers=teachers, subjects=subjects)

@views.route("/adteacher", methods=['GET', 'POST'])
def adteacher():
    if request.method == 'POST':
        details = {
            'name': request.form.get('fname') + ' ' + request.form.get('lname'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'subject': request.form.get('subject')
        }
        if details['email'] in [teacher.email for teacher in storage.all(Teacher).values()]:
            flash("The email is already registered", category='error')
        elif len(details['name']) < 7 or len(request.form.get('fname')) < 3 or len(request.form.get('lname')) < 3:
            flash("Enter a valid name", category='error')
        elif len(details['email']) < 5:
            flash("Enter a valid email", category='error')
        elif len(details['phone']) != 10 or not details['phone'].isdigit():
            flash("Enter a valid phone number", category='error')
        else:
            teacher = Teacher(**details)
            storage.new(teacher)
            storage.save()
            if details['subject'] not in [subject.name for subject in storage.all(Subject).values()]:
                new_subject = Subject(name=details['subject'], teacher_id=teacher.teacher_id)
                storage.new(new_subject)
                storage.save()
                new_subject.teacher.append(teacher)
                flash("Created new subject", category='success')
            else:
                subjects = storage.all(Subject).values()
                for subject in subjects:
                    if subject.name == details['subject']:
                        subject.teacher.append(teacher)
                        subject.teacher_id = teacher.teacher_id
                storage.save()
        return redirect(url_for("views.teachers"))

    return render_template("adteacher.html", user=current_user)

@views.route("/adstudent", methods=['GET', 'POST'])
def adstudent():
    if request.method == 'POST':
        details = {
            'name': request.form.get('fname') + ' ' + request.form.get('lname'),
            'subject': request.form.get('subject'),
            'grade': request.form.get('grade')
        }
        if details['name']in [student.name for student in storage.all(Student).values()]:
            flash("Student is already registered", category='error')
        elif len(details['name']) < 7 or len(request.form.get('fname')) < 3 or len(request.form.get('lname')) < 3:
            flash("Enter a valid name", category='error')
        elif len(details['subject']) < 3:
            flash("Enter a valid subject name", category='error')
        elif not details['grade']:
            flash("Enter the grade", category='error')
        else:
            student = Student(**details)
            storage.new(student)
            storage.save()
            if details['subject'] not in [subject.name for subject in storage.all(Subject).values()]:
                new_subject = Subject(name=details['subject'])
                storage.new(new_subject)
                storage.save()
                new_subject.student.append(student)
                storage.save()
                flash("Created new subject", category='success')
                grad = SubjectGrade(subject_id=new_subject.subject_id, student_id=student.student_id, grade=details['grade'])
                storage.new(grad)
            else:
                subjects = storage.all(Subject).values()
                for subject in subjects:
                    if subject.name == details['subject']:
                        subject.student.append(student)
                        grad = SubjectGrade(subject_id=subject.subject_id, student_id=student.student_id, grade=details['grade'])
                        storage.new(grad)
                storage.save()
        return redirect(url_for('views.students'))
    return render_template("adstudent.html", user=current_user)

@views.route("/adsubject", methods=['GET', 'POST'])
def adsubject():
    if request.method == 'POST':
        name = request.form.get('name')
        teacher_name = request.form.get('teacher_fname')+' '+request.form.get('teacher_lname')
        student_name = request.form.get('student_fname')+' '+request.form.get('student_lname')
        grades = request.form.get('grade')
        if name in [subject.name for subject in storage.all(Subject).values()]:
            flash("Subject is already registered", category='error')
        elif len(name) < 3:
            flash("Enter a valid subject name", category='error')
        elif teacher_name not in [teacher.name for teacher in storage.all(Teacher).values()]:
            flash("Teacher not registered", category='error')
        elif student_name not in [student.name for student in storage.all(Student).values()]:
            flash("Student is not registered", category='error')
        else:
            teach = None
            teachers = storage.all(Teacher).values()
            for teacher in teachers:
                if teacher.name == teacher_name:
                    teach = teacher
            stude = None
            students = storage.all(Student).values()
            for student in students:
                if student.name == student_name:
                    stude = student
            subject = Subject(name=name, teacher_id=teach.teacher_id, student_id=stude.student_id)
            storage.new(subject)
            teach.subjects.append(subject)
            stude.subjects.append(subject)
            storage.save()
            grade = SubjectGrade(grade=grades, student_id=stude.student_id, subject_id=subject.subject_id)
            storage.new(grade)
            storage.save()
            flash("New subject added", 'success')
        return redirect(url_for('views.subjects'))
    return render_template("adsubject.html", user=current_user)


@views.route("/delteacher", methods=['GET', 'POST'])
def delteacher():
    if request.method == 'POST':
        name = request.form.get('fname')+' '+request.form.get('lname')
        teacher_id = request.form.get('teacher_id')
        teachers = storage.all(Teacher).values()
        temp = None
        for teacher in teachers:
            if teacher.name == name and teacher.teacher_id == int(teacher_id):
                temp = teacher
        if temp is None:
            flash("Check the details supplied and correct them", category='error')
        else:
            storage.delete(temp)
            storage.save()
        return redirect(url_for('views.teachers'))
    return render_template("delteacher.html", user=current_user)

@views.route("/delstudent", methods=['GET', 'POST'])
def delstudent():
    if request.method == 'POST':
        name = request.form.get("fname")+' '+request.form.get('lname')
        student_id = request.form.get('student_id')
        students = storage.all(Student).values()
        temp = None
        for student in students:
            if student.name == name and student.student_id == int(student_id):
                temp = student
        if temp is None:
            flash("Check the details and ensure they are correct", category='error')
        else:
            storage.delete(temp)
            storage.save()
        return redirect(url_for('views.students'))
    return render_template("delstudents.html", user=current_user)

@views.route("/delsubject", methods=['GET', 'POST'])
def delsubject():
    if request.method == 'POST':
        name = request.form.get('name')
        subject_id = request.form.get('subject_id')
        subjects = storage.all(Subject).values()
        temp = None
        for subject in subjects:
            if subject.name == name and subject.subject_id == int(subject_id):
                temp = subject
        if temp is None:
            flash("Check the details and ensure they are correct", category='error')
        else:
            storage.delete(temp)
            storage.save()
        return redirect(url_for('views.subjects'))
    return render_template("delsubjects.html", user=current_user)

@views.route("/upteacher", methods=['GET', 'POST'])
def upteacher():
    if request.method == 'POST':
        details = {
            'name': request.form.get('fname')+' '+request.form.get('lname'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'subject': request.form.get('subject'),
            'teacher_id': request.form.get('teacher_id')
        }
        if len(details['email']) < 5:
            flash("Enter a valid email address", category='error')
        elif len(details['phone']) != 10 or not details['phone'].isdigit():
            flash("Enter a valid phone number", category='error')
        else:
            teachers = storage.all(Teacher).values()
            new = None
            sub = None
            for teacher in teachers:
                if teacher.name == details['name'] and teacher.teacher_id == int(details['teacher_id']):
                    new = teacher
            if new == None:
                flash("Enter the correct values for teacher name and teacher id", category='error')
            else:
                for key, value in details.items():
                    setattr(new, key, value)
                subjects = storage.all(Subject).values()
                for subject in subjects:
                    if subject.name == details['subject']:
                        sub = subject
                if details['subject'] not in [subject.name for subject in storage.all(Subject).values()]:
                    subject = Subject(name=details['subject'], teacher_id=new.teacher_id)
                    storage.new(subject)
                    subject.teacher.append(new)
                else:
                    sub.teacher.append(new)
                flash("Teacher Updated", category='success')
            storage.save()
        return redirect(url_for('views.teachers'))
    return render_template("upteacher.html", user=current_user)

@views.route("/upstudent", methods=['GET', 'POST'])
def upstudent():
    if request.method == 'POST':
        details = {
            'name': request.form.get("fname")+' '+request.form.get('lname'),
            'student_id': request.form.get('student_id'),
            'grade': request.form.get('grade'),
            'subject': request.form.get('subject')
        }
        if len(details['name']) < 7 or len(request.form.get('fname')) < 3 or len(request.form.get('lname')) < 3:
            flash("Enter a valid name", category='error')
        students = storage.all(Student).values()
        new = None
        for student in students:
            if student.name == details['name'] or student.student_id == int(details['student_id']):
                new = student
        if new == None:
            flash("Check the student name and sw.students.clear()tudent ID", category='error')
        else:
            for key, value in details.items():
                setattr(new, key, value)
            subjects = storage.all(Subject).values()
            for subject in subjects:
                if subject.name == details['subject']:
                    sub = subject
            if details['subject'] not in [subject.name for subject in storage.all(Subject).values()]:
                subject = Subject(name=details['subject'], teacher_id=new.teacher_id)
                storage.new(subject)
                subject.student.append(new)
            else:
                sub.student.append(new)
            grade = SubjectGrade(grade=details['grade'], student_id=new.student_id)
            storage.new(grade)
            flash("Student Updated", category='success')
        storage.save()
        return redirect(url_for('views.students'))
    return render_template("upstudent.html", user=current_user)

@views.route("/upsubject", methods=['GET', 'POST'])
def upsubject():
    if request.method == 'POST':
        details = {
            'name': request.form.get('name'),
            'subject_id': request.form.get('subject_id'),
            'teacher_name': request.form.get('teacher_fname') + ' ' + request.form.get('teacher_lname'),
            'student_name': request.form.get('student_fname') + ' ' + request.form.get('student_lname')
        }
        if len(details['teacher_name']) < 7:
            flash("Enter a valid teacher name", category='error')
        elif len(details['student_name']) < 7:
            flash("Enter a valid student name", category='error')
        subjects = storage.all(Subject).values()
        new = None
        for subject in subjects:
            if subject.name == details['name'] and subject.subject_id == int(details['subject_id']):
                new = subject
        if new is None:
            flash("Check the subject name and ID", category='error')
        else:
            for key, value in details.items():
                setattr(new, key, value)

            stude = None
            teach = None
            teachers = storage.all(Teacher).values()
            for teacher in teachers:
                if teacher.name == details['teacher_name']:
                    teach = teacher
            students = storage.all(Student).values()
            for student in students:
                if student.name == details['student_name']:
                    stude = student
            if teach is None:
                flash("Teacher not registered", category='error')
            if stude is None:
                flash("Student not registered", category='error')
            else:
                stude.subjects.append(new)
                teach.subjects.append(new)
            flash("Subject updated", category='success')
            storage.save()
        return redirect(url_for('views.subjects'))
    return render_template("upsubject.html", user=current_user)

@views.route("/users")
def users():
    users = storage.all(User).values()
    return render_template("users.html", user=current_user, users=users)

@views.route("/aduser", methods=['GET', 'POST'])
def aduser():
    if request.method == 'POST':
        details = {
            'email': request.form.get("email"),
            'first_name': request.form.get("fname"),
            'last_name': request.form.get('lname'),
            'password': request.form.get('password'),
            'password1': request.form.get('password1')
        }
        if details['email'] in [user.email for user in storage.all(User).values()]:
            flash("User already registered", 'error')
        elif len(details['email']) < 5:
            flash("Enter the valid email address", category='error')
        elif len(details['first_name']) < 3 or len(details['last_name']) < 3:
            flash("Enter a valid name", category='error')
        elif len(details['password']) < 7:
            flash("Password must be longer than 6 characters", category='error')
        elif details['password'] != details['password1']:
            flash("Passwords do not match", category='error')
        else:
            user = User(**details)
            storage.new(user)
            storage.save()
        return redirect(url_for('views.users'))
    return render_template("aduser.html", user=current_user)

@views.route("/deluser", methods=['GET', 'POST'])
def deluser():
    if request.method == 'POST':
        email = request.form.get('email')
        users = storage.all(User).values()
        for user in users:
            if user.email == email:
                storage.delete(user)
        storage.save()
        return redirect(url_for('views.users'))
    return render_template("deluser.html", user=current_user)

                        
@views.route('admnuser', methods=['GET', 'POST'])
def adnuser():
    if request.method == 'POST':
        users = storage.all(User).values()
        for user in users:
            if user.id == request.form.get('user_id'):
                user.role = 'admin'
            else:
                flash("Enter a valid user id", category='error')
        return redirect(url_for('auth.admin'))
    return render_template("admnuser.html", user=current_user)

@views.route('/about')
def about():
    return render_template('about.html', user=current_user)

@views.route("/post/new", methods=['GET', 'POST'])
@login_required
def adblog():
    form = PostForm()
    if form.validate_on_submit():
        post = Blog(title=form.title.data, content=form.content.data, author=current_user)
        storage.new(post)
        storage.save()
        flash("Your post has been created", 'success')
        return redirect(url_for('views.home'))
    return render_template('create_post.html', user=current_user, form=form, legend='New post')

@views.route("/post/<int:post_id>")
def post(post_id):
    posts = storage.all(Blog).values()
    new = None
    for post in posts:
        if post_id == post.blog_id:
            new = post
    if new == None:
        abort(404)
    return render_template('post.html', post=new, user=current_user)

@views.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def updatepost(post_id):
    posts = storage.all(Blog).values()
    new = None
    for post in posts:
        if post_id == post.blog_id:
            new = post
    if new == None:
        abort(404)
    elif new.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        new.data = form.title.data
        new.content = form.content.data
        storage.save()
        flash("Your post has been updated", 'success')
        return redirect(url_for('views.post', post_id=new.blog_id))
    elif request.method == 'GET':
        form.title.data = new.title
        form.content.data = post.content
    return render_template('create_post.html', user=current_user, form=form, legend='Update post')

@views.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    posts = storage.all(Blog).values()
    new = None
    for post in posts:
        if post_id == post.blog_id:
            new = post
    if new == None:
        abort(404)
    elif new.author != current_user:
        abort(403)
    else:
        storage.delete(new)
        storage.save()
        flash("Your post has been deleted", 'success')
        return redirect(url_for('views.home'))
    
