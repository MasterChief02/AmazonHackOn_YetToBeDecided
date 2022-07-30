import base64
from genericpath import exists
import sys
from mouseModel.addToDatabase import addToDatabase
from mouseModel.predictUpdate3 import predict
from mouseModel.trainUpdate3 import train
from faceRecogModel.project import faceRecogMain

# from AmazonHackOn_YetToBeDecided.Backend.Models.mouseModel.addToDatabase import addToDatabase
# from faceRecogModel import *
# from mouseModel import *
import numpy as np
import pandas as pd
import sys
import mysql.connector


def start():
    # s=sys.argv(5)
    s=input()
    mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="password",
        database="yettobedecided"
        )
    # print(len(sys.argv))
    mycursor = mydb.cursor()
    mycursor.execute("use yettobedecided")
    sqlFetchUserID= "select userid from users where username=%s"
    # username = (sys.argv(3),)
    username = ("aadi1",)
    mycursor.execute(sqlFetchUserID, username)
    result = mycursor.fetchall()
    id=result[0][0]
    # print(result[0][0])

    if(exists('model_pickle')):
        predict(s,id)
    else:
        addToDatabase(s,id)    
        return 1   
    print(10)

if __name__=="__main__":
    start()