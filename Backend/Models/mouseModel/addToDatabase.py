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
import math

def findDirection(x):
    if((x>=0 and x<35) or (x<0 and x>-35) ):
        return 0
    if(x>=35 and x<55):
        return 1
    if((x>=55 and x<=90) or (x>90 and x<=125)):
        return 2
    if(x>125 and x<145):
        return 3
    if((x>=145 and x<=180) or (x>=-145 and x<=-180)):
        return 4
    if(x>-145 and x<-125):
        return 5
    if(x>=-125 and x<-55):
        return 6
    if(x<=-35 and x>=-55):
        return 7
    




def addToDatabase(s,userIDKnown):
        # s=input()
        # userIDKnown = int(input())
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
        c=[]
        avgvx=[]
        avgvy=[]
        angles=[]
        directions=[0,1,2,3,4,5,6,7]
        # mvx,svx,mxvx,mnvx,mvy,svy,mxvy,mnvy,mv,sv,mxv,mnv,ma,sa,mxa,mna,mj,sj,mxj,mnj=0
        total_time=0
        total_dis_x=0
        total_dis_y=0
        X_derived = np.zeros(1*29).reshape(29)
        for i in range(0,noOfDataPoints):
            
            if i > 0:
                # print("CHECK1", X_obtained[i][1],X_obtained[i-1][1], X_obtained[i][3],  X_obtained[i-1][3])
                if((X_obtained[i][3]-X_obtained[i-1][3])==0):
                    vx.append((X_obtained[i][1] -  X_obtained[i-1][1])/(0.001))
                    vy.append((X_obtained[i][2] -  X_obtained[i-1][2])/(0.001))
                    # total_time+= (X_obtained[i][3]-X_obtained[i-1][3])
                    
                    
                else:
                    vx.append((X_obtained[i][1] -  X_obtained[i-1][1])/(X_obtained[i][3]-X_obtained[i-1][3]))
                    vy.append((X_obtained[i][2] -  X_obtained[i-1][2])/(X_obtained[i][3]-X_obtained[i-1][3]))
                total_time+= (X_obtained[i][3]-X_obtained[i-1][3])
                total_dis_x+=(X_obtained[i][1]-X_obtained[i-1][1])
                total_dis_y+=(X_obtained[i][2]-X_obtained[i-1][2])

        for i in range(len(vx)-1):
            if((X_obtained[i][3]-X_obtained[i-1][3])==0):
                ax.append((vx[i+1]-vx[i])/0.001)
                ay.append((vy[i+1]-vy[i])/0.001)
                a.append(pow((pow(ax[i],2))+(pow(ay[i],2)),(0.5)))
                
            else:
                ax.append((vx[i+1]-vx[i])/X_obtained[i+1][3]-X_obtained[i][3])
                ay.append((vy[i+1]-vy[i])/X_obtained[i+1][3]-X_obtained[i][3])
                a.append(pow((pow(ax[i],2))+(pow(ay[i],2)),(0.5)))
        
        for i in range(len(a)-1):
            if((X_obtained[i][3]-X_obtained[i-1][3])==0):
                jx.append((ax[i+1]-ax[i])/0.001)
                jy.append((ay[i+1]-ay[i])/0.001)
                j.append(pow((pow(jx[i],2))+(pow(jy[i],2)),(0.5)))
            else:
                jx.append((ax[i+1]-ax[i])/X_obtained[i+1][3]-X_obtained[i][3])
                jy.append((ay[i+1]-ay[i])/X_obtained[i+1][3]-X_obtained[i][3])
                j.append(pow((pow(jx[i],2))+(pow(jy[i],2)),(0.5)))

        for i in range(len(vx)-1):
                v.append(pow((pow(vx[i],2))+(pow(vy[i],2)),(0.5)))
        for i in range(len(vx)-1):
            avgvx.append((vx[i]+vx[i+1])/2)
            avgvy.append((vy[i]+vy[i+1])/2)

        # print(len(vx), len(vy), len(ax), len(ay), len(j), len(a))
        for i in range(len(ax)):
            c.append((ax[i]*avgvy[i] - ay[i]*avgvx[i])/(pow((avgvx[i]**2 + avgvy[i]**2),1.5)))
        
        for i in range(1,noOfDataPoints):
            myradians = math.atan2(X_obtained[i][2] -  X_obtained[i-1][2], X_obtained[i][1] -  X_obtained[i-1][1])
            mydegrees = math.degrees(myradians)
            angles.append(mydegrees)
        
        sum_of_angles=0
        for i in range(len(angles)):
            sum_of_angles+=angles[i]
        
        directions = findDirection(angles[len(angles)-1]-angles[0])

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
        sdc = statistics.stdev(c)
        mc = statistics.mean(c)
        mxc = max(c)
        mnc = min(c)
        # print("FINAL CHECK", total_dis_x, total_dis_y)
        total_distance = ((total_dis_x**2)+(total_dis_y**2))**0.5
        # X_derived[0]
        X_derived[0]=total_distance
        X_derived[1]=total_time
        X_derived[2] = directions
        X_derived[3] = sum_of_angles

        X_derived[4]=mvx
        X_derived[5]=svx
        X_derived[6]=mxvx
        X_derived[7]=mnvx
        X_derived[8]=mvy
        X_derived[9]=svy
        X_derived[10]=mxvy
        X_derived[11]=mnvy
        X_derived[12]=mv
        X_derived[13]=sv
        X_derived[14]=mxv
        X_derived[15]=mnv
        X_derived[16]=ma
        X_derived[17]=sva
        X_derived[18]=mxa
        X_derived[19]=mna
        X_derived[20]=mj
        X_derived[21]=sj
        X_derived[22]=mxj
        X_derived[23] = mnj
        X_derived[24]=mc
        X_derived[25]=sdc
        X_derived[26]=mxc
        X_derived[27]=mnc
        X_derived[28] = userIDKnown
        mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="password",
        database="yettobedecided"
        )
        print(len(sys.argv))
        mycursor = mydb.cursor()
        mycursor.execute("use yettobedecided")
        sql = "insert into derivedatt values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        mycursor.execute(sql,(float(X_derived[0]),float(X_derived[1]),float(X_derived[2]),float(X_derived[3]),float(X_derived[4]),float(X_derived[5]),float(X_derived[6]),float(X_derived[7]),float(X_derived[8]),float(X_derived[9]),float(X_derived[10]),float(X_derived[11]),float(X_derived[12]),float(X_derived[13]),float(X_derived[14]),float(X_derived[15]),float(X_derived[16]),float(X_derived[17]),float(X_derived[18]),float(X_derived[19]),float(X_derived[20]),float(X_derived[21]),float(X_derived[22]),float(X_derived[23]),float(X_derived[24]),float(X_derived[25]),float(X_derived[26]),float(X_derived[27]),float(X_derived[28])))
        mydb.commit()
if __name__ == '__main__':
    addToDatabase()      

            
