from flask import Flask,request
import pandas as pd
import numpy as np
import pickle
from titanic_problem import Sample


app=Flask(__name__) # it's a common step to start with this

# unpickle the object from the pickle file
pickle_in=open('C:/Users/Diaa Essam/OneDrive/Documents/Python/.vscode/Building A Flask App For A Model/Classifier.pkl','rb') # Reading pickle file
classifier=pickle.load(pickle_in) # taking back the object from the file

@app.route('/') # must be written to define the root page or main page to display
# this will display a web page having welcome all in it
def welcome():
    return "Welcome All"

# a page for predicting one sample, can be used through Postman
@app.route('/predict') # by default it's GET method because we will pass our features as parameters
def predict_A_sample():
    Pclass=request.args.get('Pclass')
    Name=request.args.get('Name')
    Sex=request.args.get('Sex')
    Age=request.args.get('Age')
    SibSp=request.args.get('SibSp')
    Parch=request.args.get('Parch')
    Ticket=request.args.get('Ticket')
    Fare=request.args.get('Fare')
    Cabin=request.args.get('Cabin')
    Embarked=request.args.get('Embarked')

    prediction=classifier.predict(Pclass,Name,Sex,Age,SibSp,Parch,Ticket,Fare,Cabin,Embarked)
    return "The passenger is: " + str(prediction)

# a page for predicting csv file, can be used through Postman
@app.route('/predict_file',methods=["POST"])
def predict_A_File():
    df_test=pd.read_csv(request.files.get("file")) # must be done through Postman
    prediction=classifier.predict_file(df_test)
    return "The passengers are: " + str(list(prediction))



if __name__=='__main__':
    app.run()