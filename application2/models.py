import flask
from application2 import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Document):
    user_id     =   db.IntField( unique=True )
    first_name  =   db.StringField( max_length=50 )
    last_name   =   db.StringField( max_length=50 )
    email       =   db.StringField( max_length=30, unique=True )
    password    =   db.StringField( )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)

class WorkoutSection(db.Document):
    user_id = db.IntField()
    section_title = db.StringField(max_length=50)
    meta = {
        'indexes': [
            {
                'fields': ('user_id', 'section_title'),
                'unique': True
            }
        ]
    }

class WorkoutNotes(db.Document):
    user_id = db.IntField()
    section_title = db.StringField()
    note  = db.StringField()
    created_at = db.DateTimeField()
    updated_at = db.DateTimeField()


