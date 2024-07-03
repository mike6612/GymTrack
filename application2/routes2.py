from application2 import app2, db, api
from flask import render_template, request, json, jsonify, Response, redirect, flash, url_for, session
from application2.models import User, WorkoutSection, WorkoutNotes
from application2.forms import LoginForm, RegisterForm, AddWorkoutSectionForm, AddWorkoutNoteForm
from datetime import datetime
from bson import ObjectId
from flask_restx import Resource

##########################################################
@api.route('/api','/api/')
class GetAndPost(Resource):

    #GET ALL
    def get(self):
        return jsonify(User.objects.all())

    #POST
    def post(self):
        data = api.payload
        user = User(user_id=data['user_id'], email=data['email'], first_name=data['first_name'], last_name=data['last_name'])
        user.set_password(data['password'])
        user.save()
        return jsonify(User.objects(user_id=data['user_id']))

@api.route('/api/<idx>')
class GetUpdateDelete(Resource):

    # GET ONE
    def get(self, idx):
        return jsonify(User.objects(user_id=idx))

    # PUT
    def put(self, idx):
        data = api.payload
        User.objects(user_id=idx).update(**data)
        return jsonify(User.objects(user_id=idx))

    # DELETE
    def delete(self, idx):
        User.objects(user_id=idx).delete()
        WorkoutSection.objects(user_id=idx).delete()
        WorkoutNotes.objects(user_id=idx).delete()
        return jsonify("User is deleted!")

#########################################################
@app2.route("/")
@app2.route("/index2")
@app2.route("/home")
def index2():
    return render_template("index2.html", index2=True)

@app2.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.objects(email=email).first()
        if user and user.get_password(password):
            flash(f"{user.first_name}, you are successfully logged in!", "success")
            session['user_id'] = user.user_id
            session['username'] = user.first_name
            return redirect("/index2")
        else:
            flash("Sorry, something went wrong.", "danger")
    return render_template("login.html", title="Login", form=form)

@app2.route("/logout")
def logout():
    session['user_id'] = False
    session.pop('username', None)
    return redirect(url_for('index2'))

@app2.route("/createworkoutsections", methods=['GET', 'POST'])
def createworkoutsections():
    form = AddWorkoutSectionForm()
    user_id = session.get('user_id')

    if not session.get('username'):
        flash(f"Please login or signup.", "danger")
        return redirect(url_for('login'))

    if form.validate_on_submit():
        section_title = request.form.get('section_title')
        if WorkoutSection.objects(user_id=user_id, section_title=section_title):
            flash(f"Oops! You cannot have duplicate workout section names. Please try again.", "danger")
        else:
            new_section = WorkoutSection(user_id=user_id, section_title=section_title)
            new_section.save()
            return redirect(url_for("createworkoutsections"))

    # Fetch workout sections for the user
    sections = WorkoutSection.objects(user_id=user_id)
    return render_template("createworkoutsections.html", title="My Workout Sections", sections=sections, form=form, createworkoutsections=True)

#@app2.route("/editworkoutsections", methods=['GET', 'POST'])
#def editworkoutsections():



#    user_id = session.get('user_id')
#    if not session.get('username'):
#        return redirect(url_for('login'))

#    if request.method == 'GET':
#        return render_template("editworkoutsections.html", title="My Workout Sections", editworkoutsections=True)

#    if request.method == 'POST':
#        section_title = request.form['section_title']
#        new_section = WorkSection(user_id=user_id, section_title=section_title)
#        new_section.save()
#        return redirect(url_for("edit1st"))

@app2.route("/edit1st", methods=['GET'])
def edit1st():
    user_id = session.get('user_id')
    if not session.get('username'):
        flash("Please login or signup.", "danger")
        return redirect(url_for('login'))

    sections = WorkoutSection.objects(user_id=user_id)
    return render_template("edit1st.html", sections=sections)

@app2.route("/<string:section_title>/delete", methods=['GET', 'POST'])
def delete(section_title):
    user_id = session.get('user_id')
    sections = WorkoutSection.objects(user_id=user_id, section_title=section_title).first()
    if request.method == 'POST':
        if sections:
            WorkoutNotes.objects(user_id=user_id, section_title=section_title).delete()
            sections.delete()
            return redirect('/edit1st')
        else:
            abort(404)
    
    return render_template('delete.html', sections=sections)

@app2.route("/<string:section_title>/edit", methods=['GET', 'POST'])
def update(section_title):
    sections = WorkoutSection.objects(section_title=section_title).first()
    if request.method == 'POST':
        if sections:
            section_title = request.form['section_title']
            sections.section_title = section_title
            sections.save()

            return redirect('/edit1st')
    return render_template('update.html', sections=sections)

@app2.route("/<string:section_title>/notes", methods=['GET', 'POST'])
def sectionnotes(section_title):
    user_id = session.get('user_id')


    notes = WorkoutNotes.objects(user_id=user_id, section_title=section_title)
    return render_template("sectionnotes.html", notes=notes, section_title = section_title)

@app2.route("/<string:section_title>/notes/edit/<note_id>", methods=['GET', 'POST'])
def updatenote(section_title, note_id):
    note_id = ObjectId(note_id)
    notes = WorkoutNotes.objects(id=note_id).first()

    if request.method == 'POST':
        if notes:
            note = request.form['note']
            notes.note = note
            current_time = datetime.utcnow()
            notes.updated_at = current_time.strftime('%Y-%m-%d %H:%M')
            notes.save()
            return redirect(f'/{section_title}/notes')

    return render_template('updatenote.html', notes=notes)


@app2.route("/<string:section_title>/notes/delete/<note_id>", methods=['GET', 'POST'])
def deletenote(section_title, note_id):
    note_id = ObjectId(note_id)
    note = WorkoutNotes.objects(id=note_id).first()

    if request.method == 'POST':
        if note:
            note.delete()
            return redirect(f'/{section_title}/notes')
        else:
            abort(404)
    
    return render_template('deletenote.html', note=note)

@app2.route("/createnote", methods=['GET', 'POST'])
def createnote():
    form = AddWorkoutNoteForm()
    user_id = session.get('user_id')  # Assuming user_id is stored in session

    # Check if the user is logged in
    if not session.get('username'):
        flash("Please login or signup.", "danger")
        return redirect(url_for('login'))

    # Handle form submission
    if form.validate_on_submit():
        section_title = request.form.get('section_title')

        # Check if the section title is valid
        if WorkoutSection.objects(user_id=user_id, section_title=section_title):
            note = request.form.get('note')
            current_time = datetime.utcnow()  # Get the current UTC time
            created_at = current_time.strftime('%Y-%m-%d %H:%M')
            updated_at = current_time.strftime('%Y-%m-%d %H:%M')
            # Create a new note
            new_note = WorkoutNotes(
                user_id=user_id,
                section_title=section_title,
                note=note,
                created_at=created_at,
                updated_at=updated_at
            )
            new_note.save()  # Save the note to the database

            return redirect(url_for("createnote"))
        else:
            flash("Sorry, this is not a valid workout section. Please try again.", "danger")
            return redirect(url_for('createnote'))  # Redirect back to the create note page

    # Fetch workout notes for the user if it's a GET request or form validation failed
    notes = WorkoutNotes.objects(user_id=user_id)

    return render_template("createnote.html", title="My Workout Note", notes=notes, form=form, createnote=True)

@app2.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        user_id     = User.objects.count()
        user_id     += 1

        email       = form.email.data
        password    = form.password.data
        first_name  = form.first_name.data
        last_name   = form.last_name.data

        user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        flash("You are successfully registered!","success")
        return redirect(url_for('index2'))
    return render_template("signup.html", title="Sign Up", form=form, register=True)


