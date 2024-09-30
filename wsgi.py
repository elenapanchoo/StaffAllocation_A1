import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Course, Lecturer, Tutor, TA
from App.main import create_app
from App.controllers import (
    create_user, 
    get_all_users_json, 
    get_all_users, 
    initialize,
    create_course, 
    create_lecturer, 
    create_ta, 
    create_tutor,
    assign_staff_to_course, 
    view_course_details
)

# Initialize the Flask app and migration
app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()

    # Mock Data: 
    # Lecturers
    lecturer1 = Lecturer(firstName="John", lastName="Doe")
    lecturer2 = Lecturer(firstName="Jane", lastName="Dee")
    lecturer3 = Lecturer(firstName="Emma", lastName="George")

    # TAs
    ta1 = TA(firstName="Bruce", lastName="Wayne")
    ta2 = TA(firstName="Clark", lastName="Kent")
    ta3 = TA(firstName="Peter", lastName="Parker")

    # Tutors
    tutor1 = Tutor(firstName="Miles", lastName="Morales")
    tutor2 = Tutor(firstName="Miguel", lastName="O'Hara")
    tutor3 = Tutor(firstName="Gwen", lastName="Stacy")

    db.session.add_all([
        lecturer1, lecturer2, lecturer3, 
        tutor1, tutor2, tutor3,
        ta1, ta2, ta3
    ])
    db.session.commit()

    # Courses
    course1 = Course(courseCode="COMP101", courseName="Intro to Programming", lecturer=lecturer1, tutor=tutor1, ta=ta1)
    course2 = Course(courseCode="COMP102", courseName="Data Analytics", lecturer=lecturer2, tutor=tutor2, ta=ta2)
    course3 = Course(courseCode="COMP103", courseName="Data Structures", lecturer=lecturer3, tutor=tutor3, ta=ta3)

    # Add all courses to the database
    db.session.add_all([course1, course2, course3])
    db.session.commit()

    print('Database initialized! [with mock data]')


'''
User Commands
'''

# Commands can be organized using groups
user_cli = AppGroup('user', help='User object commands') 

@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli)  # add the group to the cli

# Course Commands
course_cli = AppGroup('course', help='Course object commands')

@course_cli.command("create", help="Creates a course")
@click.argument("course_code")
@click.argument("course_name")
@click.argument("lecturer_id")
@click.argument("tutor_id")
@click.argument("ta_id")
def create_course_command(course_code, course_name, lecturer_id, tutor_id, ta_id):
    course = create_course(course_code, course_name, lecturer_id, tutor_id, ta_id)

    lecturer = Lecturer.query.get(lecturer_id)  # Use Lecturer instead of Staff
    ta = TA.query.get(ta_id)                     # Use TA instead of Staff
    tutor = Tutor.query.get(tutor_id)            # Use Tutor instead of Staff

    lecturer_name = f"{lecturer.firstName} {lecturer.lastName}" if lecturer else "None"
    tutor_name = f"{tutor.firstName} {tutor.lastName}" if tutor else "None"
    ta_name = f"{ta.firstName} {ta.lastName}" if ta else "None"

    print(f'Course {course.courseCode} created with:')
    print(f'Lecturer: {lecturer_name}')
    print(f'Tutor: {tutor_name}')
    print(f'Teaching Assistant: {ta_name}')

# Create Lecturer
@course_cli.command("create_lecturer", help="Creates a lecturer")
@click.argument("first_name")
@click.argument("last_name")
def create_lecturer_command(first_name, last_name):
    lecturer = create_lecturer(first_name, last_name)
    print(f'Lecturer {lecturer.firstName} {lecturer.lastName} created!')

# Create TA
@course_cli.command("create_ta", help="Creates a TA")
@click.argument("first_name")
@click.argument("last_name")
def create_ta_command(first_name, last_name):
    ta = create_ta(first_name, last_name)
    print(f'TA {ta.firstName} {ta.lastName} created!')

# Create Tutor
@course_cli.command("create_tutor", help="Creates a tutor")
@click.argument("first_name")
@click.argument("last_name")
def create_tutor_command(first_name, last_name):
    tutor = create_tutor(first_name, last_name)
    print(f'Tutor {tutor.firstName} {tutor.lastName} created!')

# Assign staff
@course_cli.command("assign", help="Assign staff to a course")
@click.argument("course_code")
@click.argument("lecturer_id")
@click.argument("tutor_id")
@click.argument("ta_id")
def assign_staff_command(course_code, lecturer_id, tutor_id, ta_id):
    course = Course.query.filter_by(courseCode=course_code).first()
    
    if not course:
        print(f"Course {course_code} not found!")
        return

    # Assign staff members
    course.lecturer_id = lecturer_id
    course.tutor_id = tutor_id
    course.ta_id = ta_id

    # Fetch staff details for confirmation
    lecturer = Lecturer.query.get(lecturer_id)
    tutor = Tutor.query.get(tutor_id)
    ta = TA.query.get(ta_id)

    db.session.commit()  # Commit changes to the database

    # Print out the assignment details
    print(f'Staff assigned to course {course_code}:')
    print(f'Lecturer: {lecturer.firstName} {lecturer.lastName}' if lecturer else "None")
    print(f'Tutor: {tutor.firstName} {tutor.lastName}' if tutor else "None")
    print(f'Teaching Assistant: {ta.firstName} {ta.lastName}' if ta else "None")


# View course
@app.cli.command("course view")
@click.argument("course_code")
def view_course_details(course_code):
    course = Course.query.filter_by(courseCode=course_code).first()
    
    if not course:
        print(f"Course {course_code} not found!")
        return None

    # Fetch staff details using the specific models
    lecturer = Lecturer.query.get(course.lecturer_id)
    tutor = Tutor.query.get(course.tutor_id)
    ta = TA.query.get(course.ta_id)

    # Prepare course details for display
    details = {
        "Course Code": course.courseCode,
        "Course Name": course.courseName,
        "Lecturer": f"{lecturer.firstName} {lecturer.lastName}" if lecturer else "None",
        "Tutor": f"{tutor.firstName} {tutor.lastName}" if tutor else "None",
        "Teaching Assistant": f"{ta.firstName} {ta.lastName}" if ta else "None",
    }
    
    return details

# CLI Command to view course details
@app.cli.command("course view")
@click.argument("course_code")
def view_course_command(course_code):
    """View details of a course by COURSE_CODE."""
    details = view_course_details(course_code)
    if details:
        for key, value in details.items():
            print(f"{key}: {value}")

app.cli.add_command(course_cli)

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test) 
