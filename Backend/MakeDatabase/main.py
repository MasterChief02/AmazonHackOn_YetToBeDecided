# import warnings

# from measurements.evaluate_classifier import evaluate_dataset
# from util.const import DATASET_AMOUNT
# from util.settings import CURRENT_DATASET, NUM_ACTIONS, DATASET_USAGE, NUM_TRAINING_SAMPLES

# warnings.filterwarnings('ignore', message='numpy.dtype size changed')
# warnings.filterwarnings('ignore', message='numpy.ufunc size changed')


import sys
import mysql.connector

# if __name__ == "__main__":
    
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
    mycursor.execute("create table users(userid int auto_increment primary key, username varchar(250), password varchar(250))")
    sql1 = "insert into users(username,password) values (%s, %s)"
    val1=[('aadi1','abc'),
        ('varun2', 'var123'),
        ('yogeshAI', 'passAI'),
        ('devraj2000', 'devok')]
    mycursor.executemany(sql1,val1) 
    mycursor.execute("create table mousedata(userid int , x int, y int, timestamp time, foreign key(userid) references users(userid) )")
    mycursor.execute("create table derivedAtt(userid int, traveled_distance_pixel float(5), elapsed_time float(5), mean_vx float(5), sd_vx float(5), max_vx float(5), min_vx float(5), mean_vy float(5), sd_vy float(5), max_vy float(5), min_vy float(5), mean_v float(5), sd_v float(5), max_v float(5), min_v float(5), mean_a float(5), sd_a float(5), max_a float(5), min_a float(5), mean_jerk float(5), sd_jerk float(5), max_jerk float(5), min_jerk float(5))")
    mydb.commit()
    print(mycursor.rowcount, "was inserted.")
    
    