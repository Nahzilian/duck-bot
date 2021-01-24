import datetime
from pymongo import MongoClient
from random import randint
from pprint import pprint
import time

try:
    client = MongoClient(port=27017)
    db = client.logger
except:
    print("Something went wrong with the connection, please try again")


def static_log(message: str):
    cur_time = datetime.datetime.now()
    f_loc = file_name_format(cur_time)
    f = open(f_loc,'a')
    f.write("--------------- Debug ---------------\n")
    f.write(message + '\n')
    f.write(cur_time.ctime() + '\n')
    f.close()

def file_name_format(cur_time):
    temp_str = "./log/" + cur_time.strftime("%A").lower() + "_" + cur_time.strftime("%d") + "_" + cur_time.strftime("%m") + "_" + cur_time.strftime("%Y") + ".txt"
    return temp_str

def db_logger(message: str):
    
    obj = {
        "int_time":int(time.mktime(datetime.datetime.now().timetuple())),
        "message": message,
        "time_recorded": datetime.datetime.now().ctime()
    }
    result = db.bot_log.insert_one(obj)

def log_chat(res,msg):
    obj = {
        "message": msg,
        "response": res
    }
    result = db.discord_chat.insert_one(obj)

# def load_chat():

print( )
