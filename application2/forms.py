from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application2.models import User, WorkoutSection, WorkoutNotes

class LoginForm(FlaskForm):
    email   = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6,max=15)])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    email   = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(),Length(min=6,max=15)])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(),Length(min=6,max=15), EqualTo('password')])
    first_name = StringField("First Name", validators=[DataRequired(),Length(min=2,max=55)])
    last_name = StringField("Last Name", validators=[DataRequired(),Length(min=2,max=55)])
    submit = SubmitField("Register Now")

    def validate_email(self,email):
        user = User.objects(email=email.data).first()
        if user:
            raise ValidationError("Email is already in use. Pick another one.")

class AddWorkoutSectionForm(FlaskForm):
	section_title = StringField("Workout Section Name", validators=[DataRequired(), Length(min=1, max=50)])
	submit = SubmitField("Add Section")

class AddWorkoutNoteForm(FlaskForm):
	section_title = StringField("Workout Section Name", validators=[DataRequired(), Length(min=1, max=50)])
	note  = TextAreaField("Note", validators=[DataRequired(), Length(min = 1, max = 200)])
	submit = SubmitField("Add Note")
