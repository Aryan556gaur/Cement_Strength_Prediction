import os,sys
import pymongo
import pandas as pd
import pickle
import yaml
from src.logger import logging
from src.exception import CustomException

def import_data_as_dataframe(databse,collection):
    try:
        client = pymongo.MongoClient("mongodb+srv://aryangaur556:Abhishek@cluster0.pfi4w9l.mongodb.net/?retryWrites=true&w=majority")
        coll = client[databse][collection]
        df = pd.DataFrame(coll.find())

        if "_id" in df.columns:
            df.drop("_id",axis=1,inplace=True)
    
        return df
    
    except Exception as e:
        logging.info("Error occurred in importing data")
        raise CustomException(e,sys)

def save_object(filepath:str,file_obj):
    try:
        with open(filepath,"wb") as file:
            os.makedirs(filepath,exist_ok=True)
            pickle.dump(obj=file_obj,file=file)

    except Exception as e:
        logging.info("Error occurred in saving object")
        raise CustomException(e,sys)


def read_yaml(filepath):
    try:
        with open(filepath,"rb") as file:
            return yaml.safe_load(file)
    
    except Exception as e:
        logging.info("Error occurred in loading yaml file")
        raise CustomException(e,sys)

def load_obj(filepath):
    try:
        with open(filepath,"rb") as file:
            return pickle.load(filepath)
        
    except Exception as e:
        logging.info("Error occurred in loading object")
        raise CustomException(e,sys)

