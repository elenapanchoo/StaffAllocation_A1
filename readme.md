[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/uwidcit/flaskmvc)
<a href="https://render.com/deploy?repo=https://github.com/uwidcit/flaskmvc">
  <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render">
</a>

![Tests](https://github.com/uwidcit/flaskmvc/actions/workflows/dev.yml/badge.svg)

# Flask Commands
```bash
$ flask init
```


# MOCK DATA USED

# Staff Members
| **Lecturers** | **First Name** | **Last Name** |
|---------------|----------------|---------------|
|      1        | John           | Doe           |
|      2        | Jane           | Dee           |
|      3        | Emma           | George        |

# TAs
| **TAs**        | **First Name** | **Last Name** |
|----------------|----------------|---------------|
| TA 1           | Bruce          | Wayne         |
| TA 2           | Clark          | Kent          |
| TA 3           | Peter          | Parker        |

# Tutors
| **Tutors**     | **First Name** | **Last Name** |
|----------------|----------------|---------------|
| Tutor 1        | Miles          | Morales       |
| Tutor 2        | Miguel         | O'Hara        |
| Tutor 3        | Gwen           | Stacy         |

# Courses
| **Course Code** | **Course Name**           | **Lecturer**    | **Tutor**         | **TA**           |
|-----------------|---------------------------|-----------------|-------------------|------------------|
| COMP101         | Intro to Programming       | John Doe        | Miles Morales     | Bruce Wayne      |
| COMP102         | Data Analytics             | Jane Dee        | Miguel O'Hara     | Clark Kent       |
| COMP103         | Data Structures            | Emma George     | Gwen Stacy        | Peter Parker     |


# REQUIRED COMMANDS

# 1. Create Course
```bash
$ flask course create "COURSE_CODE" "COURSE_NAME" "LECTURER_ID" "TUTOR_ID" "TA_ID"
```
For example:
```bash
$ flask course create "COMP105" "Computer Architecture" 1 3 2
```

```python

#Creating a course

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
```

# 2.Create Lecturer/TA/Tutor
```bash
$ flask course create_lecturer "first_name" "last_name"
```
```bash
$ flask course create_ta "first_name" "last_name"
```
```bash
$ flask course create_tutor "first_name" "last_name"
```
For example:
```bash
$ flask course create_lecturer "Jacob" "Jay"
```
```bash
$ flask course create_ta "Po" "Lo"
```
```bash
$ flask course create_tutor "Jamie" "Fox"
```

```python

#Create Lecturer

@course_cli.command("create_lecturer", help="Creates a lecturer")
@click.argument("first_name")
@click.argument("last_name")
def create_lecturer_command(first_name, last_name):
    lecturer = create_lecturer(first_name, last_name)
    print(f'Lecturer {lecturer.firstName} {lecturer.lastName} created!')

#Create TA

@course_cli.command("create_ta", help="Creates a TA")
@click.argument("first_name")
@click.argument("last_name")
def create_ta_command(first_name, last_name):
    ta = create_ta(first_name, last_name)
    print(f'TA {ta.firstName} {ta.lastName} created!')

#Create Tutor

@course_cli.command("create_tutor", help="Creates a tutor")
@click.argument("first_name")
@click.argument("last_name")
def create_tutor_command(first_name, last_name):
    tutor = create_tutor(first_name, last_name)
    print(f'Tutor {tutor.firstName} {tutor.lastName} created!')
```

# 3.Assign Lecturer/TA/Tutor to Course
```bash
$ flask course assign "COURSE_CODE" "LECTURER_ID" "TUTOR_ID" "TA_ID"
```

For example:
```bash
$ flask course assign "COMP101" 1 1 1
```

```python

#Assign staff

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

    #Assign staff members
    course.lecturer_id = lecturer_id
    course.tutor_id = tutor_id
    course.ta_id = ta_id

    #Fetch staff details for confirmation
    lecturer = Lecturer.query.get(lecturer_id)
    tutor = Tutor.query.get(tutor_id)
    ta = TA.query.get(ta_id)

    db.session.commit()  

    # Print out the assignment details
    print(f'Staff assigned to course {course_code}:')
    print(f'Lecturer: {lecturer.firstName} {lecturer.lastName}' if lecturer else "None")
    print(f'Tutor: {tutor.firstName} {tutor.lastName}' if tutor else "None")
    print(f'Teaching Assistant: {ta.firstName} {ta.lastName}' if ta else "None")
```

# 4.View Course Staff
```bash
$ flask course view "COURSE_CODE"
```

For example:
```bash
$ flask course view "COMP101"
```

```python

#Viewing Courses

@course_cli.command("view", help="View course details")
@click.argument("course_code")
def view_course_details_command(course_code):
    course = Course.query.filter_by(courseCode=course_code).first()
    
    if not course:
        print(f"Course {course_code} not found!")
        return

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
    
    # Print details instead of returning
    print("Course Details:")
    for key, value in details.items():
        print(f"{key}: {value}")
```

