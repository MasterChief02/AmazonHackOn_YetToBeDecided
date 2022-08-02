import base64
from genericpath import exists
import sys, os
from mouseModel.addToDatabase import addToDatabase
from mouseModel.predictUpdate3 import predict
from mouseModel.main import main as mouse_distance
from Face_Recognition import face_recognition
from Key_Logger import key_logger
from Multi_Model import multi_model
import numpy as np
import pandas as pd
import sys
import mysql.connector


def start():
    
    
    # s=input()
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
    username = (sys.argv[3],)
    sqlFetchPassword = "select password from users where username=%s"
    # username = ("aadi1",)
    mycursor.execute(sqlFetchUserID, username)
    result = mycursor.fetchall()
    user_id=0
    password=''
    if(len(result)==0):
        print(10)
        
    else:
        user_id = result[0][0]
        mycursor.execute(sqlFetchPassword, username)
        result = mycursor.fetchall()
        password = result[0][0]


        mouse_string = sys.argv[1]
        temp = sys.stdout
        sys.stdout = open(os.devnull, "w")
        print(mouse_string)
        mouse_value = mouse_distance(mouse_string, user_id)
        print("Mouse Value: ", mouse_value)
        # Login
        if (len(sys.argv)==4):
            face_value = face_recognition.face_distance(1)
            # face_value=0
            key_logger_value = key_logger.string_distance(sys.argv[3],password)
            multi_model_value = multi_model.predict(mouse_value, face_value, key_logger_value)
        sys.stdout = temp
        print("Mouse: ", mouse_value, " Face:", face_value, " Key:", key_logger_value, " Overall:",  multi_model_value)

if __name__=="__main__":
    start()