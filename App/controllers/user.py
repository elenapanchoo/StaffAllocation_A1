from App.models import User, Course, Lecturer, TA, Tutor
from App.database import db

def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None



def create_course(course_code, course_name, lecturer_id, tutor_id, ta_id):
    # Check if the course already exists
    existing_course = Course.query.filter_by(courseCode=course_code).first()
    if existing_course:
        raise Exception(f"Course with courseCode '{course_code}' already exists.")
    
    # Create a new course if it doesn't exist
    new_course = Course(courseCode=course_code, courseName=course_name, lecturer_id=lecturer_id, tutor_id=tutor_id, ta_id=ta_id)
    db.session.add(new_course)
    db.session.commit()
    
    return new_course


def create_lecturer(first_name, last_name):
    lecturer = Lecturer(firstName=first_name, lastName=last_name)
    db.session.add(lecturer)
    db.session.commit()
    return lecturer

def create_ta(first_name, last_name):
    ta = TA(firstName=first_name, lastName=last_name)
    db.session.add(ta)
    db.session.commit()
    return ta

def create_tutor(first_name, last_name):
    tutor = Tutor(firstName=first_name, lastName=last_name)
    db.session.add(tutor)
    db.session.commit()
    return tutor

def assign_staff_to_course(course_code, lecturer_id=None, tutor_id=None, ta_id=None):
    course = Course.query.filter_by(courseCode=course_code).first()
    if not course:
        return False  # Course not found

    if lecturer_id:
        course.lecturer_id = lecturer_id
    if tutor_id:
        course.tutor_id = tutor_id
    if ta_id:
        course.ta_id = ta_id

    db.session.commit()
    return True

def view_course_details(course_code):
    course = Course.query.filter_by(courseCode=course_code).first()
    if not course:
        return "Course not found."

    lecturer = Staff.query.get(course.lecturer_id)
    tutor = Staff.query.get(course.tutor_id)
    ta = Staff.query.get(course.ta_id)

    return {
        "Course Code": course.courseCode,
        "Course Name": course.courseName,
        "Lecturer": f"{lecturer.firstName} {lecturer.lastName}" if lecturer else "None",
        "Tutor": f"{tutor.firstName} {tutor.lastName}" if tutor else "None",
        "Teaching Assistant": f"{ta.firstName} {ta.lastName}" if ta else "None"
    }
