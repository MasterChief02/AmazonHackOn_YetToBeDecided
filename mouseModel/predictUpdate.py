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
    # with open('test.csv','r') as csv_file:
    #     csv_reader=csv.reader(csv_file)
    #     next(csv_reader)
        # data_list = list(csv.reader(csv_reader))
        s=input()
        userIDKnown = int(input())
        ls=s.split(",")
        noOfDataPoints= int(len(ls)/3)
        X_obtained = np.zeros(4*noOfDataPoints).reshape(noOfDataPoints,4)
        index=0
        for i in range(noOfDataPoints):
                # print(index,noOfDataPoints)
                X_obtained[i][1] = ls[index]
                X_obtained[i][2] = ls[index+1]
                X_obtained[i][3] = ls[index+2]
                index+=3
       
        # count=0
        

        # for i in csv_reader:
        #     # print(type(i))
        #     if(count < 10):
        #         print(len(i))
        #         # noOfDataPoints+=1
        #         print(i[0],i[1],i[2],"MAJOR CHECK")
        #         X_obtained[count][3] = i[0]
        #         X_obtained[count][1] = i[1]
        #         X_obtained[count][2] = i[2]
        #         print(X_obtained[count][3],"ACCHA")
        #         count+=1
        #     else:
        #         break
       
          
            
        # print(X_obtained,"CHECK00")
        vx=[]
        vy=[]
        ax=[]
        ay=[]
        jx=[]
        jy=[]
        a=[]
        j=[]
        v=[]
        # mvx,svx,mxvx,mnvx,mvy,svy,mxvy,mnvy,mv,sv,mxv,mnv,ma,sa,mxa,mna,mj,sj,mxj,mnj=0
        total_time=0
        total_dis_x=0
        total_dis_y=0
        X_derived = np.zeros(1*23).reshape(23)
        for i in range(0,noOfDataPoints-1):
            
            if i > 0:
                # print("CHECK1", X_obtained[i][1],X_obtained[i-1][1], X_obtained[i][3],  X_obtained[i-1][3])
                if((X_obtained[i][3]-X_obtained[i-1][3])==0):
                    vx.append((X_obtained[i][1] -  X_obtained[i-1][1])/(0.000001))
                    vy.append((X_obtained[i][2] -  X_obtained[i-1][2])/(0.000001))
                    # total_time+= (X_obtained[i][3]-X_obtained[i-1][3])
                    
                    
                else:
                    vx.append((X_obtained[i][1] -  X_obtained[i-1][1])/(X_obtained[i][3]-X_obtained[i-1][3]))
                    vy.append((X_obtained[i][2] -  X_obtained[i-1][2])/(X_obtained[i][3]-X_obtained[i-1][3]))
                total_time+= (X_obtained[i][3]-X_obtained[i-1][3])
                total_dis_x+=(X_obtained[i][1]-X_obtained[i-1][1])
                total_dis_y+=(X_obtained[i][2]-X_obtained[i-1][2])

        for i in range(len(vx)-1):
            if((X_obtained[i][3]-X_obtained[i-1][3])==0):
                ax.append((vx[i+1]-vx[i])/0.0001)
                ay.append((vy[i+1]-vy[i])/0.0001)
                
            else:
                ax.append((vx[i+1]-vx[i])/X_obtained[i+1][3]-X_obtained[i][3])
                ay.append((vy[i+1]-vy[i])/X_obtained[i+1][3]-X_obtained[i][3])
                a.append(pow((pow(ax[i],2))+(pow(ay[i],2)),(0.5)))
        
        for i in range(len(a)-1):
            if((X_obtained[i][3]-X_obtained[i-1][3])==0):
                jx.append((ax[i+1]-vx[i])/0.00001)
                jy.append((ay[i+1]-vy[i])/0.00001)
            else:
                jx.append((ax[i+1]-vx[i])/X_obtained[i+1][3]-X_obtained[i][3])
                jy.append((ay[i+1]-vy[i])/X_obtained[i+1][3]-X_obtained[i][3])
                j.append(pow((pow(jx[i],2))+(pow(jy[i],2)),(0.5)))

        for i in range(len(vx)-1):
                v.append(pow((pow(vx[i],2))+(pow(vy[i],2)),(0.5)))
        


        svx=statistics.stdev(vx)
        svy=statistics.stdev(vy)
        mvx=statistics.mean(vx)
        mvy=statistics.mean(vy)
        mnvx = min(vx)
        mxvx = max(vx)
        mnvy = min(vy)
        mxvy = max(vy)
        sv = statistics.stdev(v)
        mv = statistics.mean(v)
        mxv=max(v)
        mnv = min(v)
        sva = statistics.stdev(a)
        ma = statistics.mean(a)
        mxa = max(a)
        mna = min(a)
        sj = statistics.stdev(j)
        mj = statistics.mean(j)
        mxj = max(j)
        mnj = min(j)
        # print("FINAL CHECK", total_dis_x, total_dis_y)
        total_distance = ((total_dis_x**2)+(total_dis_y**2))**0.5
        # X_derived[0]
        X_derived[1]=total_distance
        X_derived[2]=total_time
        X_derived[3]=mvx
        X_derived[4]=svx
        X_derived[5]=mxvx
        X_derived[6]=mnvx
        X_derived[7]=mvy
        X_derived[8]=svy
        X_derived[9]=mxvy
        X_derived[10]=mnvy
        X_derived[11]=mv
        X_derived[12]=sv
        X_derived[13]=mxv
        X_derived[14]=mnv
        X_derived[15]=ma
        X_derived[16]=sva
        X_derived[17]=mxa
        X_derived[18]=mna
        X_derived[19]=mj
        X_derived[20]=sj
        X_derived[21]=mxj
        X_derived[22]=mnj

        X_derived=X_derived.reshape(1,-1)
        # print(X_derived)
        useridObtained = mp.predict(X_derived)
        y_scores = mp.predict_proba(X_derived)
        max_y_score = max(y_scores[0])
        # print(y_scores.shape)
        relation_with_given_user = y_scores[0][userIDKnown-1]
        print("This user matches max with")
        print(y_scores)
        print("Score with given id: ")
        print(relation_with_given_user)
        X_derived[0] = useridObtained

        print(useridObtained, "This is the predicted user id")
        userIDKnown=7
        if(useridObtained==userIDKnown):
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

        

            
