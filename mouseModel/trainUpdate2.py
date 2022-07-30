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

# def evaluate_sequence_of_samples(model, X_validation, y_validation, num_actions):
#     # print(len(X_validation))
#     if num_actions == 1:
#         y_scores = model.predict_proba(X_validation)
#         # writeCSVa(y_validation, y_scores[:, 1])
#         return roc_curve(y_validation, y_scores[:, 1])

#     X_val_positive = []
#     X_val_negative = []
#     for i in range(len(y_validation)):
#         if y_validation[i] == 1:
#             X_val_positive.append(X_validation[i])
#         else:
#             X_val_negative.append(X_validation[i])
#     pos_scores = model.predict_proba(X_val_positive)
#     neg_scores = model.predict_proba(X_val_negative)

#     scores =[]
#     labels =[]

#     n_pos = len(X_val_positive)
#     for i in range(n_pos-num_actions+1):
#         score = 0
#         for j in range(num_actions):
#             score += pos_scores[i+j][1]
#         score /= num_actions
#         scores.append(score)
#         labels.append(1)

#     n_neg = len(X_val_negative)
#     for i in range(n_neg - num_actions + 1):
#         score = 0
#         for j in range(num_actions):
#             score += neg_scores[i + j][1]
#         score /= num_actions
#         scores.append(score)
#         labels.append(0)

#     # writeCSVa(labels, scores)
#     return roc_curve(labels, scores)

if __name__ == '__main__':
    mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="password",
        database="yettobedecided"
        )
    print(len(sys.argv))
    mycursor = mydb.cursor()
    mycursor.execute("use yettobedecided")

    
    NoOfFeat=27
    fpr = {}
    tpr = {}
    roc_auc = {}

    sql = "select * from derivedatt"
    mycursor.execute(sql)
    records = mycursor.fetchall()

    NoOfUsers = 0
    for rows in records:
        NoOfUsers+=1
    X_train = np.zeros(NoOfUsers*27).reshape(NoOfUsers,27)
    Y_train = np.zeros(NoOfUsers).reshape(NoOfUsers)
    
    for j in range(0,NoOfUsers):
        for i in range(0,27):
            if i<26:
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

    # fpr[i], tpr[i], thr = evaluate_sequence_of_samples(model, X_validation, y_validation, 2)

    # threshold = -1
    # try:
    #     eer = brentq(lambda x: 1. - x - interp1d(fpr[i], tpr[i])(x), 0., 1.)
    #     threshold = interp1d(fpr[i], thr)(eer)
    # except (ZeroDivisionError, ValueError):
    #     print("Division by zero")

    # roc_auc[i] = auc(fpr[i], tpr[i])
    # print(str(i) + ": " + str(roc_auc[i])+" threshold: "+str(threshold))
    with open('model_pickle','wb') as f:
        pickle.dump(model,f)


