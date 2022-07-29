import numpy as np
import pandas as pd
import sys
import mysql.connector
import pickle
from sklearn import model_selection, metrics
from sklearn.metrics import roc_curve, auc, roc_auc_score, accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate
TEST_SIZE = 0.33
import statistics
import csv

if __name__ == '__main__':
    with open('model_pickle','rb') as f:
        mp = pickle.load(f)

    # mydb = mysql.connector.connect(
    #     host="localhost",
    #     user="admin",
    #     password="password",
    #     database="yettobedecided"
    #     )
    # print(len(sys.argv))
    # mycursor = mydb.cursor()
    # mycursor.execute("use yettobedecided")

    # sql = "select * from mousedata"
    # mycursor.execute(sql)
    # records = mycursor.fetchall()
    with open('test.csv','r') as csv_file:
        csv_reader=csv.reader(csv_file)
        next(csv_reader)

        noOfDataPoints=0

        for i in csv_reader:
            noOfDataPoints+=1

        X_obtained = np.zeros(4*noOfDataPoints).reshape(noOfDataPoints,4)
        for i in range(0,noOfDataPoints):
            for j in range(0,4):
                X_obtained[i][j] = csv_reader[i][j]

        vx=[]
        vy=[]
        ax=[]
        ay=[]
        jx=[]
        jy=[]
        a=[]
        j=[]
        mvx,svx,mxvx,mnvx,mvy,svy,mxvy,mnvy,mv,sv,mxv,mnv,ma,sa,mxa,mna,mj,sj,mxj,mnj=0
        total_time=0
        total_dis_x=0
        total_dis_y=0
        X_derived = np.zeros(1*23).reshape(1,23)
        for i in range(0,noOfDataPoints):
            
            if i > 0:
                vx.append(X_obtained[i][1] -  X_obtained[i-1][1])/(X_obtained[i][3]-X_obtained[i-1][3])
                vy.append(X_obtained[i][2] -  X_obtained[i-1][2])/(X_obtained[i][3]-X_obtained[i-1][3])
                total_time+=X_obtained[i][3]-X_obtained[i-1][3]
                total_dis_x+=X_obtained[i][1]-X_obtained[i-1][1]
                total_dis_y+=X_obtained[i][2]-X_obtained[i-1][2]

        for i in range(len(vx)-1):
            ax.append((vx[i+1]-vx[i])/X_obtained[i+1][3]-X_obtained[i][3])
            ay.append((vy[i+1]-vy[i])/X_obtained[i+1][3]-X_obtained[i][3])
            a.append(pow((pow(ax[i],2))+(pow(ay[i],2)),(0.5)))
        
        for i in range(len(a)-1):
            jx.append((ax[i+1]-vx[i])/X_obtained[i+1][3]-X_obtained[i][3])
            jy.append((ay[i+1]-vy[i])/X_obtained[i+1][3]-X_obtained[i][3])
            j.append(pow((pow(jx[i],2))+(pow(jy[i],2)),(0.5)))

        svx=statistics.stdev(vx)
        svy=statistics.stdev(vy)
        mvx=statistics.mean(vx)
        mvy=statistics.mean(vy)
        mnvx = min(vx)
        mxvx = max(vx)
        mnvy = min(vy)
        mxvy = max(vy)
        sva = statistics.stdev(a)
        ma = statistics.mean(a)
        mxa = max(a)
        mna = min(a)
        sj = statistics.stdev(j)
        mj = statistics.mean(j)
        mxj = max(j)
        mnj = min(j)
        total_distance = pow((pow(total_dis_x,0.5),pow(total_dis_y,0.5)),(0.5))
        # X_derived[0]
        X_derived[0]=total_distance
        X_derived[1]=total_time
        X_derived[2]=mvx
        X_derived[3]=svx
        X_derived[4]=mxvx
        X_derived[5]=mnvx
        X_derived[6]=mvy
        X_derived[7]=svy
        X_derived[8]=mxvy
        X_derived[9]=mnvy
        X_derived[10]=mv
        X_derived[11]=sv
        X_derived[12]=mxv
        X_derived[13]=mnv
        X_derived[14]=ma
        X_derived[15]=sa
        X_derived[16]=mxa
        X_derived[17]=mna
        X_derived[18]=mj
        X_derived[19]=sj
        X_derived[20]=mxj
        X_derived[21]=mnj

        useridObtained = mp.predict(X_derived)
        X_derived[22] = useridObtained
        print(useridObtained)
        if(useridObtained==X_obtained[0][0]):
            mydb = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="password",
            database="yettobedecided"
            )
            print(len(sys.argv))
            mycursor = mydb.cursor()
            mycursor.execute("use yettobedecided")
            sql = "insert into derivedatt values(X_derived[0],X_derived[1],X_derived[2],X_derived[3],X_derived[4],X_derived[5],X_derived[6],X_derived[7],X_derived[8],X_derived[9],X_derived[10],X_derived[11],X_derived[12],X_derived[13],X_derived[14],X_derived[15],X_derived[16],X_derived[17],X_derived[18],X_derived[19],X_derived[20],X_derived[21],X_derived[22])"
        else:
            print("Wrong user detected")
        # mxvx = v=x
        
        # 
        #     vx = (X_obtained[i][1] -  X_obtained[i-1][1])/(X_obtained[i][3]-X_obtained[i-1][3])
        #     if(vx>mxvx):
        #         mxvx=vx
        #     mvx=vx
        # if i>1:
        #     mvx = ((mvx*i-1)+vx)/i
        

            
