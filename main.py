from flask import Flask, request, render_template, send_from_directory
import sqlite3 as lite
import models
import os
import jinja2
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home_page.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('txtName')
        fun_fact = request.form.get('txtFunFact')
        tribe = request.form.get('txtTribe')
        image_file = request.files['fileToUpload']
        job_title = request.form.get('txtJobTitle')

        filename = secure_filename(image_file.filename)
        image_file.save(os.path.join('Images', filename))
        models.add_to_db(str(name), str(fun_fact), str(tribe), filename, str(job_title))

        return '<h1> Success </h1>'

    return render_template('UploadImage.html')


@app.route('/squad_display')
def squad():
    db = lite.connect("Photo Card Database.db")
    c = db.cursor()
    c.execute('SELECT * from Photo_Card')
    Squads = [dict(ID=row[0],
                   Name=row[1],
                   Tribe=row[2],
                   Image=row[3],
                   JobTitle=row[4],
                   FunFact=row[5]) for row in c.fetchall()]

    return render_template("squad_display.html", Squads=Squads)


@app.route('/squad_individual_SUS+')
def squad_sus():
    Squads = squad_individual_display("SUS+")
    return render_template("squad_individual.html", Squads=Squads)


@app.route('/squad_individual_CIS')
def squad_cis():
    Squads = squad_individual_display("CIS (Care Identity Service)")
    return render_template("squad_individual.html", Squads=Squads)


@app.route('/squad_individual_HES')
def squad_hes():
    Squads = squad_individual_display("HES")
    return render_template("squad_individual.html", Squads=Squads)


@app.route('/squad_individual_SPINE')
def squad_spine():
    Squads = squad_individual_display("SpineCore")
    return render_template("squad_individual.html", Squads=Squads)


def squad_individual_display(individual_type):
    db = lite.connect("Photo Card Database.db")
    c = db.cursor()
    c.execute('''SELECT * FROM Photo_Card WHERE Tribe = ?''', (individual_type,))
    Squads = [dict(ID=row[0],
                   Name=row[1],
                   Tribe=row[2],
                   Image=row[3],
                   JobTitle=row[4],
                   FunFact=row[5]) for row in c.fetchall()]
    return Squads


if __name__ == '__main__':
    app.run(debug=True)
