import numpy as np
import pandas as pd
import sys
import mysql.connector
import pickle
from sklearn import model_selection, metrics
from sklearn.metrics import roc_curve, auc, roc_auc_score, accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate
from itertools import cycle
from sklearn import model_selection, metrics
from sklearn.metrics import roc_curve, auc, roc_auc_score, accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate

# from plot import plotROCs
# # from util.settings import *
# # from util.process import *
# # from util.const import *

from scipy.optimize import brentq
from scipy.interpolate import interp1d
from sklearn.metrics import roc_curve
TEST_SIZE = 0.33

def train():
    mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="password",
        database="yettobedecided"
        )
    print(len(sys.argv))
    mycursor = mydb.cursor()
    mycursor.execute("use yettobedecided")

    
    NoOfFeat=29
    fpr = {}
    tpr = {}
    roc_auc = {}

    sql = "select * from derivedatt"
    mycursor.execute(sql)
    records = mycursor.fetchall()

    NoOfUsers = 0
    for rows in records:
        NoOfUsers+=1
    X_train = np.zeros(NoOfUsers*29).reshape(NoOfUsers,29)
    Y_train = np.zeros(NoOfUsers).reshape(NoOfUsers)
    
    for j in range(0,NoOfUsers):
        for i in range(0,29):
            if i<28:
                X_train[j][i] = records[j][i]
            else:
                Y_train[j] = records[j][i]
    
    X_train, X_validation, y_train, y_validation = model_selection.train_test_split(X_train, Y_train, test_size=TEST_SIZE,random_state=0)
    model = RandomForestClassifier(random_state= 0)
    model.fit(X_train, y_train)

    scores = cross_validate(model, X_train, y_train, cv=10, return_train_score=False)
    cv_accuracy = scores['test_score']
    print("CV Accuracy: %0.2f (+/- %0.2f)" % (cv_accuracy.mean(), cv_accuracy.std() * 2))

    y_predicted = model.predict(X_validation)
    test_accuracy = accuracy_score(y_validation, y_predicted)
    test_accuracy = accuracy_score(y_validation, y_predicted)
    print("Test Accuracy: %0.2f" % test_accuracy)

    with open('model_pickle','wb') as f:
        pickle.dump(model,f)

if __name__ == '__main__':
    train()
