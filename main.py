import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donor, Donation 

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/', methods=['GET'])
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.jinja2')

    if request.method == 'POST':
        # I tried adding a try/except block to check names being added but
        # was not able to get it to work correctly as the name being checked
        # always seemed to make it into the db first (causing IndexOutOfRange error)
        # and there seemed to be no way that I could devise to check it/catch it
        # before it caused problems
        donor = Donor.select().where(Donor.name == request.form['name']).get()
        donation = Donation(donor=donor, value=float(request.form['value']))
        donation.save()
        return redirect(url_for('home')) 
    else:
        return render_template('create.jinja2')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
