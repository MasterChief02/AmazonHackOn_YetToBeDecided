import numpy as np
import pandas as pd
import sys
import mysql.connector
if __name__== '__main__' :
    df = pd.read_csv(r'C:/Users/Aaditya Gupta/OneDrive/Desktop/balabit_39feat_PC_MM_DD_100.csv')
    print(df.head())
    mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="password",
        database="yettobedecided"
        )
    print(len(sys.argv))
    mycursor = mydb.cursor()
    mycursor.execute("use yettobedecided")
    for i,row in df.iterrows():
        #here %S means string values 
        sql = "INSERT INTO derivedatt VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        mycursor.execute(sql, tuple(row))
        print("Record inserted")
        # the connection is not auto committed by default, so we must commit to save our changes
        mydb.commit()
    sql = "select * from derivedatt"
    mycursor.execute(sql)
    mydb.commit()