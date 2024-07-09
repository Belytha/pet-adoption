"""Adopt application"""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm
app = Flask(__name__)

app.config['SECRET_KEY'] = "abcdef"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

with app.app_context():
        db.drop_all()
        db.create_all()


@app.route("/")
def home():
    """Displays home page which is a list of pets"""
    pets = Pet.query.all()
    return render_template("pet_list.html", pets=pets)

@app.route("/add", methods=['GET', 'POST'])
def add_pet():
    """Adds a pet"""
    form = AddPetForm()
    if form.validate_on_submit():
        new_pet = Pet(name=form.name.data, species=form.species.data, age=form.age.data, photo_url=form.photo_url.data, notes=form.notes.data)
        db.session.add(new_pet)
        db.session.commit()
        return redirect("/")
        
    return render_template('add_pet_form.html', form=form)

@app.route("/<int:pet_id>", methods=['GET', 'POST'])
def display_pet(pet_id):

    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data
        db.session.commit()
        return redirect("/")
    else:
        return render_template('display-pet.html', pet=pet, form=form)