import numpy as np
import os
import pandas as pd
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import inspect
from flask import Flask, request, jsonify, render_template, redirect
from flask_restful import Resource, Api, reqparse
import pickle


# import psycopg2
# from flask_migrate import Migrate


# ###############################################
# #Database setup
# ###############################################

# database_path = "../Resources/fr.sqlite"
# engine = create_engine(f"sqlite:///{database_path}")

# # Declare a Base using automap_base()
# Base = automap_base()

# # Reflect the tables
# Base.prepare(engine, reflect=True)

# save reference to each table
# gender_parity = Base.classes.gender_parity
# national_data = Base.classes.national_data
# occupation = Base.classes.sorted_occupation
# states_data = Base.classes.states_data

###############################################
#Flask setup
###############################################
app = Flask(__name__)
api=Api(app)
print("\nInitiating flask server...")

from flask_sqlalchemy import SQLAlchemy
# engine = create_engine("sqlite:///Resources/SQLDB.sqlite")

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') 


# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/female_representation_db"
# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# db-to-sqlite "postgresql://postgres:postgres@localhost:5432/female_representation_db" fr.db \
#     --all

data_arg=reqparse.RequestParser()
data_arg.add_argument("id" , type=str)
# load ML model
model=pickle.load(open('model.pkl', 'rb'))
class predict(Resource):
    def __init__(self):
        self.model1 = model
    def post(self):
        # parse data from post request
        args = data_arg.parse_args()
        # convert string into int list
        temp=args.id.strip('][').split(',')
        temp = [float(i) for i in temp]
        # predict output
        out=self.model1.predict([temp])
        # Return prediction
        return jsonify({"message":  int(out)})
api.add_resource(predict, '/')

###############################################
# Flask Routes
###############################################
@app.route("/")
def index():

    return render_template("index.html")

@app.route("/national")
def national():
    return render_template("prediction.html")

@app.route("/state")
def state():

    return render_template("state.html")



@app.route("/casestudy")
def casestudy():

    return render_template("casestudy.html")
   
    

###What do we want for DATA page??###

@app.route("/data")
def data():

    return {"hello":"world"}

@app.route("/predict")
def predict():

    return {"Insert":"ML"}


if __name__ == "__main__":
    app.run(debug=True)