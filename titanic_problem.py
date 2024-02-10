# -*- coding: utf-8 -*-
"""titanic_problem.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CGHuEagwr1BJinLlAydYfCWWYdRVhtoN

# Importing the libraries
"""

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from imblearn.pipeline import make_pipeline
import os
import warnings
warnings.filterwarnings('ignore')

current_directory = os.path.abspath(os.path.dirname(__file__))
train_path = os.path.join(current_directory, "Data", "train.csv")
test_path = os.path.join(current_directory, "Data", "test.csv")
"""# Importing the Datasets"""

train_data=pd.read_csv(train_path)
train_data.head()
train_data.shape

test_data_org=test_data=pd.read_csv(test_path)
print(test_data.head())
test_data.shape

"""# Taking Ground Truth from Train Data"""

y=train_data['Survived'].values
y.shape

"""# Merging Train Data and Test Data"""

train_data=train_data.drop(['Survived'], axis=1)
concated_data=pd.concat([train_data,test_data],ignore_index=True)

"""# Feature Engineering"""

concated_data['Relatives'] = concated_data['SibSp'] + concated_data['Parch']
concated_data.loc[concated_data['Relatives'] > 0, 'Alone'] = 0
concated_data.loc[concated_data['Relatives'] == 0, 'Alone'] = 1

"""# Checking Nan values"""

#Thanks to this notebook (https://www.kaggle.com/code/gunesevitan/titanic-advanced-feature-engineering-tutorial)
for col in concated_data.columns.tolist():
    print('{} column missing values: {}'.format(col, concated_data[col].isnull().sum()))

# Thanks to this notebook (https://www.kaggle.com/code/gunesevitan/titanic-advanced-feature-engineering-tutorial)
concated_data[concated_data['Embarked'].isnull()]

"""# Now fix these values:"""

concated_data['Embarked'] = concated_data['Embarked'].fillna('S')

"""# Feature Selection"""

X=concated_data[['Pclass','Sex','Age','SibSp','Parch','Fare','Embarked','Relatives']].values
print(X[0:5,:])

"""# Taking care of missing data"""

from sklearn.impute import SimpleImputer
imputer=SimpleImputer(missing_values=np.nan, strategy='mean')

imputer.fit(X[:,2].reshape(-1,1))
X[:,2]=(imputer.transform(X[:,2].reshape(-1,1))).reshape(-1,)

imputer.fit(X[:,5].reshape(-1,1))
X[:,5]=(imputer.transform(X[:,5].reshape(-1,1))).reshape(-1,)

"""# Encoding Categorical Data"""

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
ct=ColumnTransformer(transformers=[('encoder',OneHotEncoder(),[6])],remainder='passthrough')
X=np.array(ct.fit_transform(X))

from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
X[:,4]=le.fit_transform(X[:,4])


"""# Getting back Train data and Test data"""

test_data=X[891:]
X=X[:891]

"""# Splitting the Data"""

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(X,y,test_size=0.25,random_state=1)

print(x_train[:6])

print(x_test[:6])

print(y_train[:6])

print(y_test[:6])

print(x_train.shape,x_test.shape, y_train.shape, y_test.shape)

"""# Feature Scaling"""

from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
x_train[:,3:]=sc.fit_transform(x_train[:,3:])
x_test[:,3:]=sc.transform(x_test[:,3:])
test_data[:,3:]=sc.transform(test_data[:,3:])

print(x_train[:6])

print(x_test[:6])

"""# Applying Kernel PCA"""

from sklearn.decomposition import PCA
pca=PCA(n_components=6)
x_train=pca.fit_transform(x_train)
x_test=pca.transform(x_test)
test_data=pca.transform(test_data)

"""# K-Fold Cross Validation"""

# Used to make sure that We do not get lucky on easy examples in the training set and measure the real Accuracy
def K_Fold_CV(model):
    pipeline = make_pipeline(model)
    scores = cross_val_score(pipeline, X=x_train, y=y_train, cv=10, n_jobs=1)
    print('Cross Validation accuracy: %.3f +/- %.3f' % (np.mean(scores),np.std(scores)))
    return (np.mean(scores))

"""# Hyperparameter Tuning"""

# Used to find the best hyperparameters for a given model
def best_param(model,param_grid):
    gs=GridSearchCV(model,param_grid,cv=10)
    gs.fit(x_train,y_train)
    print("best params: ",gs.best_params_)

"""# Confusion Matrix"""

best_Acc={

    }
def Confusion_Matrix(y_pred,name):
    cm=confusion_matrix(y_test,y_pred)
    print(cm)
    print("")
    print("Sum of Wrong predictions",cm[0,1]+cm[1,0])
    print("Accuracy of the model: ",accuracy_score(y_test,y_pred))
    best_Acc[name]=accuracy_score(y_test,y_pred)

"""# Checking the Overfitting"""

def check_Overfitting(yhat_test,model):
    yhat_train=model.predict(x_train)
    return accuracy_score(y_train,yhat_train),accuracy_score(y_test,yhat_test)

"""# Kernel SVM"""

from sklearn.svm import SVC
# finiding the best parameters using GridSearchCV
param_grid=[{'C': [0.25, 0.5, 0.75, 1], 'kernel': ['linear']},
              {'C': [0.25, 0.5, 0.75, 1], 'kernel': ['rbf'], 'gamma': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]}]

best_param(SVC(random_state=1),param_grid)

classifier_SVM=SVC(C=0.75,gamma=0.1,kernel='rbf')
classifier_SVM.fit(x_train,y_train)

y_pred_SVM = classifier_SVM.predict(x_test)
y_pred_TD_SVM=classifier_SVM.predict(test_data)
print((np.concatenate((y_pred_SVM.reshape(len(y_pred_SVM),1), y_test.reshape(len(y_test),1)),1))[:20])

concatenated_array=(np.concatenate((y_pred_SVM.reshape(len(y_pred_SVM),1), y_test.reshape(len(y_test),1)),1))
print(concatenated_array[(concatenated_array[:,0]!=concatenated_array[:,1])])

Confusion_Matrix(y_pred_SVM,"Kernel SVM")

# a class for testing samples
class Sample:

    # function to test a single sample
    def predict(self,Pclass,Name,Sex,Age,SibSp,Parch,Ticket,Fare,Cabin,Embarked):
        Relatives=SibSp + Parch
        x=np.array([Pclass,Sex,Age,SibSp,Parch,Fare,Embarked,Relatives]).reshape(1,-1)

        x=np.array(ct.transform(x))

        x[:,4]=le.transform(x[:,4])

        x[:,3:]=sc.transform(x[:,3:])

        x=pca.transform(x)

        return classifier_SVM.predict(x)

    # function to predict a CSV file
    def predict_file(self,df_test):

    # handling preprocessing operations
        df_test['Relatives'] = df_test['SibSp'] + df_test['Parch']
        df_test.loc[df_test['Relatives'] > 0, 'Alone'] = 0
        df_test.loc[df_test['Relatives'] == 0, 'Alone'] = 1

        df_test['Embarked'] = df_test['Embarked'].fillna('S')

        test=df_test[['Pclass','Sex','Age','SibSp','Parch','Fare','Embarked','Relatives']].values

        imputer.fit(test[:,2].reshape(-1,1))
        test[:,2]=(imputer.transform(test[:,2].reshape(-1,1))).reshape(-1,)

        imputer.fit(test[:,5].reshape(-1,1))
        test[:,5]=(imputer.transform(test[:,5].reshape(-1,1))).reshape(-1,)

        test=np.array(ct.fit_transform(test))

        test[:,4]=le.fit_transform(test[:,4])

        test[:,3:]=sc.transform(test[:,3:])

        test=pca.transform(test)
        return classifier_SVM.predict(test)



test_sample=Sample()
print(test_sample.predict(1,'diaa','female',60,1,0,'Australia',15.22,'C105','Q'))

# look in the note
pickle_file_path = os.path.join(current_directory, "Classifier.pkl")

import pickle
pickle_out=open(pickle_file_path,"wb")
pickle.dump(test_sample, pickle_out)
pickle_out.close()
