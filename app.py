import numpy as np
import os
import pandas as pd
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import inspect
from flask import Flask, request, jsonify, render_template, redirect
import pickle


###############################################
#Flask setup
###############################################

app = Flask(__name__)
# api=Api(app)
print("\nInitiating flask server...")

from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') 


# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/female_representation_db"
# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# db-to-sqlite "postgresql://postgres:postgres@localhost:5432/female_representation_db" fr.db \
#     --all

# data_arg=reqparse.RequestParser()
# data_arg.add_argument("id" , type=str)
# # load ML model
# model=pickle.load(open('model.pkl', 'rb'))
# class predict(Resource):
#     def __init__(self):
#         self.model1 = model
#     def post(self):
#         # parse data from post request
#         args = data_arg.parse_args()
#         # convert string into int list
#         temp=args.id.strip('][').split(',')
#         temp = [float(i) for i in temp]
#         # predict output
#         out=self.model1.predict([temp])
#         # Return prediction
#         return jsonify({"message":  int(out)})
# api.add_resource(predict, '/')

###############################################
# Flask Routes
###############################################
@app.route("/")
def index():

    return render_template("index.html")

@app.route("/national")
def national():

    return render_template("national.html")

@app.route("/state")
def state():

    return render_template("state.html")

# @app.route("/prediction")
# def prediction():

#     return render_template("prediction.html")

@app.route("/prediction", methods=["GET", "POST"])
def prediction():

    # If the user fills out our form, assign variables to their inputs and run the machine learning model function.
    if request.method == "POST":
        occ = request.form["occupation"]
        gndr = request.form["gender"]
        yr = request.form["year"]

        # also need to do these things, but not sure where:
        # call predictml function/route with occ, gndr, and year as inputs
        # save the function's output as something we can then cause to display in
        # prediction.html "answer" element (currently line 41). Do we need a .js script for that?

        # return redirect("/", code=302) # don't think we need this, it was from pet pals example
        # return predictml(occ, gndr, yr) # this may be what we'll need but predictml() doesn't do anything and idk what format the input needs to be in.

    return render_template("prediction.html")


@app.route("/data")
def data():

    return render_template("data.html")

@app.route("/predictml")
def predictml():
    # 1. load model
    # 2. y = model.predict  # pass user inputs from prediction.html as input to predict function here
    # 3. return y

    return {"Insert":"ML function"}


if __name__ == "__main__":
    app.run(debug=True)