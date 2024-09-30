from App.database import db

class Course(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    courseCode = db.Column(db.String(120), nullable=False, unique=True)
    courseName = db.Column(db.String(120), nullable=False)

    lecturer_id = db.Column(db.Integer, db.ForeignKey('lecturer.id'), nullable=False)
    ta_id = db.Column(db.Integer, db.ForeignKey('ta.id'))
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'))

    lecturer = db.relationship('Lecturer', backref='courses')
    ta = db.relationship('TA', backref='courses')
    tutor = db.relationship('Tutor', backref='courses')



