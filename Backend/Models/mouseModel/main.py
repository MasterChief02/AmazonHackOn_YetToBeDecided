import base64
from genericpath import exists
import sys
from mouseModel.addToDatabase import addToDatabase
from mouseModel.predictUpdate3 import predict

# from AmazonHackOn_YetToBeDecided.Backend.Models.mouseModel.addToDatabase import addToDatabase
# from faceRecogModel import *
# from mouseModel import *
import numpy as np
import pandas as pd
import sys
import mysql.connector
import os.path
def main(s,id):
    if(os.path.exists('/mnt/ntfs/Projects/Hackathon/AmazonHackOn_YetToBeDecided/model_pickle')):
        # print("HERE",id)
        return predict(s,id)
        # print("HERE1")
    else:
        # print("DEKHIO")
        addToDatabase(s,id)
        # print("DEKHIO2.0")
        return 1
