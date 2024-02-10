from flask import Flask,request
import pandas as pd
import pickle
from titanic_problem import Sample
from flasgger import Swagger
import os


app=Flask(__name__) # it's a common step to start with this
Swagger(app) # pass the App to Swagger

# unpickle the object from the pickle file
current_directory = os.path.abspath(os.path.dirname(__file__))
pickle_file_path = os.path.join(current_directory, "Classifier.pkl")

pickle_in=open(pickle_file_path,'rb') # Reading pickle file
classifier=pickle.load(pickle_in) # taking back the object from the file

@app.route('/') # must be written to define the root page or main page to display
# this will display a web page having welcome all in it
def welcome():
    return "Welcome All"

# a page for predicting one sample, can be used through Postman
@app.route('/predict',methods=["POST"]) # by default it's GET method because we will pass our features as parameters
def predict_A_sample():
    """
    Let's see who will survive
    ---
    parameters:
        - name: Pclass
          in: query
          schema:
            type: number
            enum: [1, 2, 3]
            example: 3
        - name: Name
          in: query
          type: string
        - name: Sex
          in: query
          schema:
            type: string
            enum: [male, female, Male,Female]
            example: male
        - name: Age
          in: query
          type: number
        - name: SibSp
          in: query
          type: boolean
        - name: Parch
          in: query
          type: boolean
        - name: Ticket
          in: query
          type: string
        - name: Fare
          in: query
          type: number
        - name: Cabin
          in: query
          type: string
        - name: Embarked
          in: query
          schema:
            type: string
            enum: [Q, S, C]
            example: C

    responses:
        200:
            description: The output value

    """
    Pclass=request.args.get('Pclass')
    Name=request.args.get('Name')
    Sex=request.args.get('Sex').lower()
    Age=request.args.get('Age')
    SibSp=request.args.get('SibSp')
    SibSp= 1 if SibSp=='true' else 0
    Parch=request.args.get('Parch')
    Parch=1 if Parch=='true' else 0
    Ticket=request.args.get('Ticket')
    Fare=request.args.get('Fare')
    Cabin=request.args.get('Cabin')
    Embarked=request.args.get('Embarked')


    prediction=classifier.predict(Pclass,Name,Sex,Age,SibSp,Parch,Ticket,Fare,Cabin,Embarked)
    return "The passenger survived" if prediction[0]==1 else "The passenger didn't survived"

# a page for predicting csv file, can be used through Postman
@app.route('/predict_file',methods=["POST"])
def predict_A_File():

    """
    Let's see who will survive
    ---
    parameters:
        - name: file
          in: formData
          type: file
          required: true
    
    responses:
        200:
            description: The output values
    """
    df_test=pd.read_csv(request.files.get("file")) # must be done through Postman
    prediction=classifier.predict_file(df_test)
    return "The passengers are: " + str(list(prediction))



if __name__=='__main__':
    app.run()
