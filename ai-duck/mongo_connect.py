from pymongo import MongoClient
from random import randint
from pprint import pprint
import json

is_error = False
# Pre-load database
try:
    client = MongoClient(port=27017)
    db = client.chatapp
except:
    print("Something went wrong with the connection, please try again")

def create_new_tag(tag:str, patterns:list, responses:list):
    """
    Create new tag and add to database
    """
    if is_error:
        print("No tag could be made due to connection error")
    else:
        obj = {
            "tag": tag,
            "patterns": patterns,
            "responses": responses,
            "context_set": ""
        }
        result = db.chatapp.insert_one(obj)
        print(f'Added {result}')


def load_db():
    """
    Return data from database
    """
    result = []
    if not is_error:
        result = db.chatapp.find({})
    return result


def update_tag(data_type: str,new_data: str,tag: str,remove_type: bool):
    """
    Update data based on tag
    """
    if is_error:
        print("Data cannot be updated due to connection error")
    else:
        mongo_command = '$addToSet'
        if remove_type == True:
            mongo_command = '$pull'
        selected_data = db.chatapp.find_one({'tag':tag})
        if data_type == 'tag':
            result = db.chatapp.update_one({'_id': selected_data.get('_id')}, {'$set': {'tag': new_data}})
            pprint(result)
        elif data_type == 'patterns':
            result = db.chatapp.update_one({'_id': selected_data.get('_id')}, {mongo_command: {'patterns': new_data}})
        elif data_type == 'responses':
            result = db.chatapp.update_one({'_id': selected_data.get('_id')}, {mongo_command: {'responses': new_data}})
        else:
            print("update type was not found")
