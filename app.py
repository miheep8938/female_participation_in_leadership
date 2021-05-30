import numpy as np
import pandas as pd
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, request, jsonify, render_template
import psycopg2



# ###############################################
# #Database setup
# ###############################################



engine = create_engine("sqlite:///Resources/SQLDB.sqlite")

# Declare a Base using automap_base()
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# save reference to each table
gender_parity = Base.classes.gender_parity
national_data = Base.classes.national_data
occupation = Base.classes.sorted_occupation
states_data = Base.classes.states_data

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

@app.route("/apitest")
def testing():
    # Create our session from Python to the DB
    session = Session(engine) 

# #     """Convert the query results to a dictionary using date as the key and prcp as the value"""
# #     """Return the JSON representation of your dictionary."""

# #     recent_year = dt.date(2017, 8 ,23)
# #     # Calculate the date one year from the last date in data set.
# #     previous_year = recent_year - dt.timedelta(days=365)
    test_query = session.query(national_data).all()
    state = test_query
    session.close()

    return jsonify(state)
    




if __name__ == "__main__":
    app.run(debug=True)