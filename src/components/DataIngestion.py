import os,sys
import pandas as pd
from dataclasses import dataclass
from src.utils import import_data_as_dataframe
from src.logger import logging
from src.exception import CustomException
from sklearn.model_selection import train_test_split

@dataclass
class DataIngestionConfig:
    Raw_data_path = os.path.join("artifacts","raw_data.csv")
    train_data_path = os.path.join("artifacts","train.csv")
    test_data_path = os.path.join("artifacts","test.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_ingestion(self):

        try:
            logging.info("Data ingestion starts")

            df = import_data_as_dataframe("database","Cement_Strength_Prediction")

            os.makedirs(self.ingestion_config.Raw_data_path,exist_ok=True)

            df.to_csv(self.ingestion_config.Raw_data_path,header=True,index=False)

            train_data, test_data = train_test_split(df,test_size=0.25,random_state=42)

            train_data.to_csv(self.ingestion_config.train_data_path,header=True,index=False)
            test_data.to_csv(self.ingestion_config.test_data_path,header=True,index=False)

            logging.info("Data ingestion successful")

            return self.ingestion_config.Raw_data_path
    
        except Exception as e:
            logging.info("Error occurred in Data Ingestion")
            raise CustomException(e,sys)
        
if __name__=="__main__":
    obj=DataIngestion()
    raw_data =obj.initiate_ingestion()