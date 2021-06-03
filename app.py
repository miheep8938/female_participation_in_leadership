from flask_sqlalchemy import SQLAlchemy
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
from joblib import load


###############################################
# Flask setup
###############################################

app = Flask(__name__)

print("\nInitiating flask server...")
pipeline = load('model3.joblib')

# form validation function for text fields
def ReplaceChars(text):
    if text is "" or text is None:
        text = 0  # if text box is empty default the value to 0
    else:
        chars = ",$"  # removing common monetary and numeric formatting
        for c in chars:
            text = text.replace(c, '')
        if '.' in text:
            # typecasting to float then to int to drop the decimal places
            text = int(float(text))
    return text


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')

# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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


@app.route("/prediction", methods=['POST', 'GET'])
def prediction():
    # Return template and data

    # take user input from Form as a Post request and typecast it to the proper data structure
    if request.method == 'POST':
        try:
            user_age = int(ReplaceChars(int(request.form['user_age'])))
        except ValueError:
            return render_template('prediction.html', title="Salary Prediction", decision="Invalid input on age field.")
        
        try:
            user_workhour = int(ReplaceChars(
                str(request.form['user_workhour'])))
        except ValueError:
            return render_template('prediction.html', title="Salary Prediction", decision="Invalid input on workhour field.")

        user_gender = int(request.form['user_gender'])
        user_employment = int(request.form['user_employment'])
        if user_employment == 0:
            employment_private = 1
            employment_public = 0
            employment_self = 0
            employment_unemployed = 0
        elif user_employment == 1:
            employment_private = 0
            employment_public = 1
            employment_self = 0
            employment_unemployed = 0
        elif user_employment == 2:
            employment_private = 0
            employment_public = 0
            employment_self = 1
            employment_unemployed = 0
        else:
            employment_private = 0
            employment_public = 0
            employment_self = 0
            employment_unemployed = 1

        user_education = int(request.form['user_education'])
        if user_education == 0:
            employment_highschool = 1
            employment_associate = 0
            employment_bachelors = 0
            employment_graduate = 0
            employment_not_graduated = 0
            employment_preschool = 0
        elif user_education == 1:
            employment_highschool = 0
            employment_associate = 1
            employment_bachelors = 0
            employment_graduate = 0
            employment_not_graduated = 0
            employment_preschool = 0
        elif user_education == 2:
            employment_highschool = 0
            employment_associate = 0
            employment_bachelors = 1
            employment_graduate = 0
            employment_not_graduated = 0
            employment_preschool = 0
        elif user_education == 3:
            employment_highschool = 0
            employment_associate = 0
            employment_bachelors = 0
            employment_graduate = 1
            employment_not_graduated = 0
            employment_preschool = 0
        elif user_education == 4:
            employment_highschool = 0
            employment_associate = 0
            employment_bachelors = 0
            employment_graduate = 0
            employment_not_graduated = 1
            employment_preschool = 0
        else:
            employment_highschool = 0
            employment_associate = 0
            employment_bachelors = 0
            employment_graduate = 0
            employment_not_graduated = 0
            employment_preschool = 1

        user_marital = int(request.form['user_marital'])
        if user_marital == 0:
            employment_single = 1
            employment_married = 0
            employment_separated = 0
            employment_divorced = 0
            employment_widowed = 0
        elif user_marital == 1:
            employment_single = 0
            employment_married = 1
            employment_separated = 0
            employment_divorced = 0
            employment_widowed = 0
        elif user_marital == 2:
            employment_single = 0
            employment_married = 0
            employment_separated = 1
            employment_divorced = 0
            employment_widowed = 0
        elif user_marital == 3:
            employment_single = 0
            employment_married = 0
            employment_separated = 0
            employment_divorced = 1
            employment_widowed = 0
        else:
            employment_single = 0
            employment_married = 0
            employment_separated = 0
            employment_divorced = 0
            employment_widowed = 1

        user_occupation = int((request.form['user_occupation']))
        if user_occupation == 0:
            employment_manager = 1
            employment_service = 0
            employment_sales = 0
            employment_technician = 0
            employment_agricultural = 0
            employment_clerical = 0
        elif user_occupation == 1:
            employment_manager = 0
            employment_service = 1
            employment_sales = 0
            employment_technician = 0
            employment_agricultural = 0
            employment_clerical = 0
        elif user_occupation == 2:
            employment_manager = 0
            employment_service = 0
            employment_sales = 1
            employment_technician = 0
            employment_agricultural = 0
            employment_clerical = 0
        elif user_education == 3:
            employment_manager = 0
            employment_service = 0
            employment_sales = 0
            employment_technician = 1
            employment_agricultural = 0
            employment_clerical = 0
        elif user_occupation == 4:
            employment_manager = 0
            employment_service = 0
            employment_sales = 0
            employment_technician = 0
            employment_agricultural = 1
            employment_clerical = 0
        else:
            employment_manager = 0
            employment_service = 0
            employment_sales = 0
            employment_technician = 0
            employment_agricultural = 0
            employment_clerical = 1

        user_ethnicity = int((request.form['user_ethnicity']))
        if user_ethnicity == 0:
            employment_white = 1
            employment_black = 0
            employment_asian = 0
            employment_aboriginal = 0
        elif user_ethnicity == 1:
            employment_white = 0
            employment_black = 1
            employment_asian = 0
            employment_aboriginal = 0
        elif user_ethnicity == 2:
            employment_white = 0
            employment_black = 0
            employment_asian = 1
            employment_aboriginal = 0
        else:
            employment_white = 0
            employment_black = 0
            employment_asian = 0
            employment_aboriginal = 1

        user_continent = int((request.form['user_continent']))
        if user_continent == 0:
            employment_NA = 1
            employment_SA = 0
            employment_Asia = 0
            employment_EU = 0
        elif user_continent == 1:
            employment_NA = 0
            employment_SA = 1
            employment_Asia = 0
            employment_EU = 0
        elif user_continent == 2:
            employment_NA = 0
            employment_SA = 0
            employment_Asia = 1
            employment_EU = 0
        else:
            employment_NA = 0
            employment_SA = 0
            employment_Asia = 0
            employment_EU = 1



        # put the variables into a pandas dataframe
        df = pd.DataFrame({
            'age': [user_age],
            'workhour': [user_workhour],
            'sex_ Male': [user_gender],
            'workclass_ Government': [employment_public],
            'workclass_ Private': [employment_private],
            'workclass_ Self': [employment_self],
            'workclass_ Without': [employment_unemployed],

            'education_ High_School_Degree': [employment_highschool],
            'education_ Associate_Degree': [employment_associate],
            'education_ Bachelors': [employment_bachelors],
            'education_ Graduate': [employment_graduate],
            'workclass_ Not_Graduated': [employment_not_graduated],
            'workclass_ Preschool': [employment_preschool],

            'marital _Single': [employment_single],
            'marital _Married': [employment_married],
            'marital _Separated': [employment_separated],
            'marital _Divorced': [employment_divorced],
            'marital _widowed': [employment_widowed],
            
            
            
            'occupation _Managerial': [employment_manager],
            'occupation _Service': [employment_service],
            'occupation _Sales': [employment_sales],
            'occupation _Technical': [employment_technician],
            'occupation _Agricultural': [employment_agricultural],
            'occupation _Clerical': [employment_clerical],


            'race_ White': [employment_white],
            'race_ Black': [employment_black],
            'race_ Asian': [employment_asian],
            'race_ Aboriginal': [employment_aboriginal],



            'location_ North_America': [employment_NA],
            'location_ South_America': [employment_SA],
            'location_ Asia': [employment_Asia],
            'location_ Europe': [employment_EU]
        })

        pred_cols = list(df.columns.values)
        prediction = pipeline.predict(df[pred_cols])[0]
        if prediction == 0:
            decision = 'Denied'
        if prediction == 1:
            decision = 'Approved'

        return render_template('prediction.html', title="Salary Prediction", decision=decision)

    decision = "Fill out the form on the left."
    return render_template("prediction.html", title="Salary Prediction", decision=decision)


@app.route("/data")
def data():

    return render_template("data.html")


@app.route("/predictml")
def predictml():

    return {"Insert": "ML function"}


if __name__ == "__main__":
    app.run(debug=True)
