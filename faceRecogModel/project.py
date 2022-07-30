from cgi import test
import cv2
import numpy as np
import face_recognition as fr
import os
import sys
import mysql.connector

path = 'ImageDataBase'
images = []
classnames = []
myList = os.listdir(path)
print(myList)

for cl in myList:
    cur = cv2.imread(f'{path}/{cl}')
    images.append(cur)
    classnames.append(os.path.splitext(cl)[0])

mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="password",
        database="yettobedecided"
        )
print(len(sys.argv))
mycursor = mydb.cursor()
mycursor.execute("use yettobedecided")


print(classnames)

def findEnncodings(images):
    encoded = []
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = fr.face_encodings(img)[0]
        encoded.append(encode)

    return encoded

def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)

encodeKnown = findEnncodings(images)

pathT = 'TESTImage'
myListT = os.listdir(pathT)
imageTest=[]
for cl in myListT:
    curTest = cv2.imread(f'{pathT}/{cl}')

    # curTest = cv2.cvtColor(curTest,cv2.COLOR_BGR2RGB)
    
    facLoc = fr.face_locations(curTest)[0]
    encode = fr.face_encodings(curTest)[0]
    

    matches = fr.compare_faces(encodeKnown,encode)
    faceDis = fr.face_distance(encodeKnown, encode)
    matchindex = np.argmin(faceDis)
    # print(matchindex)
    if matches[matchindex]:

            name = classnames[matchindex].upper()
            # print(name)
            y1,x2,y2,x1 = facLoc
            # y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(curTest,(x1,y1),(x2,y2),(0,255,0),2)
            # cv2.rectangle(img,(x1,y1+35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(curTest,name,(x1+6,y2+6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            # 
            print("Valid User")
            cv2.imshow('User', curTest)
            cv2.waitKey(0)
    else:
            y1,x2,y2,x1 = facLoc
            # y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(curTest,(x1,y1),(x2,y2),(0,0,255),2)
            # cv2.rectangle(img,(x1,y1+35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(curTest,"FAKE",(x1+6,y2+6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            # cv2.waitKey(10000)
            cv2.imshow('Fake user', curTest)
            cv2.waitKey(0)


'''
cap  = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0,0), None, 0.25,0.25)
    imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

    facLocCur = fr.face_locations(imgS)
    encodeCur = fr.face_encodings(imgS,facLocCur)

    for encodeFace, faceLoc in zip(encodeCur,facLocCur):
        matches = fr.compare_faces(encodeKnown,encodeFace)
        faceDis = fr.face_distance(encodeKnown, encodeFace)
        print(faceDis)
        matchindex = np.argmin(faceDis)
        
        if matches[matchindex]:

            name = classnames[matchindex].upper()
            print(name)
            y1,x2,y2,x1 = faceLoc
            y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            # cv2.rectangle(img,(x1,y1+35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2+6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            # cv2.waitKey(10000)
            print("Valid User")
            # exit
        else:
            y1,x2,y2,x1 = faceLoc
            y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),2)
            # cv2.rectangle(img,(x1,y1+35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,"FAKE",(x1+6,y2+6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            # cv2.waitKey(10000)
            print("Fake user")
            # exit

    
    cv2.imshow('Webcam', img)
'''

    
    
            
