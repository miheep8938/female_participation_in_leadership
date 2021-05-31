import numpy as np
import pandas as pd
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import inspect
from flask import Flask, request, jsonify, render_template
import psycopg2



# ###############################################
# #Database setup
# ###############################################



engine = create_engine("sqlite:///Resources/female_representation_db.sqlite")

# Declare a Base using automap_base()
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# save reference to each table
# gender_parity = Base.classes.gender_parity
# national_data = Base.classes.national_data
# occupation = Base.classes.sorted_occupation
# states_data = Base.classes.states_data

###############################################
#Flask setup
###############################################
app = Flask(__name__)
print("\nInitiating flask server...")

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



@app.route("/casestudy")
def casestudy():

    return render_template("casestudy.html")
   
    

###What do we want for DATA page??###


if __name__ == "__main__":
    app.run(debug=True)