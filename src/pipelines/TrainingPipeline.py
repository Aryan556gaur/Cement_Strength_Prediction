import os,sys
from src.components.DataIngestion import DataIngestion
from src.components.DataTransformation import DataTransformation
from src.components.ModelTrainer import ModelTrainer
from src.logger import logging
from src.exception import CustomException

class TrainingPipeline:
    def __init__(self):
        self.data_ingestion = DataIngestion()
        self.data_transformation = DataTransformation()
        self.model_trainer = ModelTrainer()

    def run_training_pipeline(self):

        try:
            logging.info("Training Pipeline Execution starts")

            raw_data_path = self.data_ingestion.initiate_ingestion()
            x_train,x_test,y_train,y_test = self.data_transformation.initiate_Transformation(Raw_data_path=raw_data_path)
            self.model_trainer.initiate_training(x_train,x_test,y_train,y_test)

        except Exception as e:
            logging.info("Exception occurred in Training Pipeline")
            raise CustomException(e,sys)
