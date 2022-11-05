from application import app 
from flask import render_template, Flask, redirect, request, url_for
import pandas as pd
import numpy as np
import pickle

#importing data 
data = pd.read_csv('bank.csv')
#importing clean data
clean = pd.read_csv('cleaned.csv')
#importing pickle file
pickle_in = pickle.load(open('finalised_model.pkl', 'rb'))
#creating a fucntion for the prediction
def load_model(converted_values):
    predicted_values = pickle_in.predict([converted_values])
    return predicted_values
#rawdata columns
raw_data_columns = data.columns
#cleaned data columns
cleaned_data_columns = clean.columns 
#pickle file columns
pickle_file_columns = pickle_in.feature_names_in_

#getting the unique values from the raw data
raw_data_unique_values = []
for raw in raw_data_columns:
    for col in pickle_file_columns:
        if raw == col:
            raw_data_unique_values.append(data[raw].unique())

#converting to string to make the distonary
raw_data_unique_values_string = []
for number in range(len(raw_data_unique_values)):
    for num in raw_data_unique_values[number]:
        convert_string = str(num)
        raw_data_unique_values_string.append(convert_string)

#getting the unique values for the cleaned data
cleaned_data_unique_values = []
for cleans in cleaned_data_columns:
    for col in pickle_file_columns:
        if cleans == col:
            cleaned_data_unique_values.append(clean[cleans].unique())
#converting to the string cleaned data nique values
clean_data_unique_values_string = []
for number in range(len(cleaned_data_unique_values)):
    for num in cleaned_data_unique_values[number]:
        convert_string = str(num)
        clean_data_unique_values_string.append(convert_string)
#making a distonary
orginal_data = raw_data_unique_values_string
clean_data = clean_data_unique_values_string
result = {}
for orginal in orginal_data:
    for clean in clean_data:
        result[orginal] = clean
        clean_data.remove(clean)
        break
#creating a array for the pickle file columns
cols = []
for column in pickle_file_columns:
    cols.append(column)
#getting the length of the picklefile columns
length = len(pickle_file_columns)

@app.route("/", methods = ['GET', 'POST'])
def index():
    converted_values = []
    if request.method == 'POST':
        if request.form.get('action1') == 'Submit':
            condition = True
            for ran in range(length):
                con_string = str(ran)
                each_data = request.form[con_string]
                results = result[each_data]
                converted_values.append(results)
        predicted_results = load_model(converted_values)
        if predicted_results == 0:
            predicted_results = 'No'
        elif predicted_results == 1:
            predicted_results = 'Yes'
        else:
            predicted_results = "Error"
        return render_template('index.html', pickle_file_columns=pickle_file_columns, length=length, 
    raw_data_unique_values=raw_data_unique_values, predicted_results=predicted_results, condition=condition)

    return render_template('index.html', pickle_file_columns=pickle_file_columns, length=length, 
    raw_data_unique_values=raw_data_unique_values)



#delete_list = request.form.getlist('my_checkbox')