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

def main(s,id):
    if(exists('model_pickle')):
        predict(s,id)
    else:
        addToDatabase(s,id)
        return 1

