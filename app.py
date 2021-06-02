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
# Flask setup
###############################################

app = Flask(__name__)
# api=Api(app)
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


# engine = create_engine("sqlite:///Resources/SQLDB.sqlite")


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


@app.route("/prediction", methods=['POST', 'GET'])
def prediction():
    # Return template and data

    # take user input from Form as a Post request and typecast it to the proper data structure
    if request.method == 'POST':
        # try:
        #     user_gender = int(ReplaceChars(str(request.form['user_gender'])))
        # except ValueError:
        #     return render_template('prediction.html', title="Salary Prediction", decision="Invalid input on Gender field.")
        try:
            user_age = int(ReplaceChars(int(request.form['user_age'])))
        except ValueError:
            return render_template('prediction.html', title="Salary Prediction", decision="Invalid input on age field.")
        # try:
        #     user_employment = int(ReplaceChars(str(request.form['user_employment'])))
        # except ValueError:
        #     return render_template('prediction.html', title="Salary Prediction", decision="Invalid input on employment field.")
        # try:
        #     user_education = int(ReplaceChars(str(request.form['user_education'])))
        # except ValueError:
        #     return render_template('prediction.html', title="Salary Prediction", decision="Invalid input on education field.")
        # try:
        #     user_marital = int(ReplaceChars(str(request.form['user_marital'])))
        # except ValueError:
        #     return render_template('prediction.html', title="Salary Prediction", decision="Invalid input on marital status field.")
        # try:
        #     user_occupation = int(ReplaceChars(str(request.form['user_occupation'])))
        # except ValueError:
        #     return render_template('prediction.html', title="Salary Prediction", decision="Invalid input on occupation field.")
        # try:
        #     user_ethnicity = int(ReplaceChars(str(request.form['user_ethnicity'])))
        # except ValueError:
        #     return render_template('prediction.html', title="Salary Prediction", decision="Invalid input on ethnicity field.")
        try:
            user_workhour = int(ReplaceChars(
                str(request.form['user_workhour'])))
        except ValueError:
            return render_template('prediction.html', title="Salary Prediction", decision="Invalid input on workhour field.")
        # try:
        #     user_continent = int(ReplaceChars(str(request.form['user_continent'])))
        # except ValueError:
        #     return render_template('prediction.html', title="Salary Prediction", decision="Invalid input on continent field.")

##################################################
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

# user_employment = int(ReplaceChars(str(request.form['user_employment'])))
        # loan_amount_term = int(request.form['loan_amount_term'])
        # credit_history = int(request.form['credit_history'])
        # gender = int(request.form['gender'])
        # married = int(request.form['married'])

        # dependents = int(request.form['dependents'])
        # if dependents == 0:
        #     dependents_zero = 1
        #     dependents_one = 0
        #     dependents_two = 0
        #     dependents_three = 0
        # elif dependents == 1:
        #     dependents_zero = 0
        #     dependents_one = 1
        #     dependents_two = 0
        #     dependents_three = 0
        # elif dependents == 2:
        #     dependents_zero = 0
        #     dependents_one = 0
        #     dependents_two = 1
        #     dependents_three = 0
        # else:
        #     dependents_zero = 0
        #     dependents_one = 0
        #     dependents_two = 0
        #     dependents_three = 1
        # # education = int(request.form['education'])
        # # self_employed = int(request.form['self_employed'])
        # property_area = int(request.form['property_area'])
        # if property_area == 0:
        #     rural = 1
        #     semiurban = 0
        #     urban = 0
        # elif property_area == 1:
        #     rural = 0
        #     semiurban = 1
        #     urban = 0
        # else:
        #     rural = 0
        #     semiurban = 0
        #     urban = 1

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
