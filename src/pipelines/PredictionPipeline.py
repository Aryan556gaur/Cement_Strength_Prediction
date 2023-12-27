import os,sys
import pandas as pd
import numpy as np
from src.pipelines.TrainingPipeline import TrainingPipeline
from src.logger import logging
from src.exception import CustomException
from src.utils import load_obj
from flask import request

class PredictionConfig:
    prediction_file_path = os.path.join("artifacts","prediction.csv")
    preprocessor_path = os.path.join("artifacts","preprocessor.pkl")
    model_path = os.path.join("artifacts","model.pkl")

class SinglePrediction:
    def __init__(self, Cement, Blast, Fly, Water, Superplasticizer, Coarse, Fine, Age):
        self.Cement = Cement
        self.Blast = Blast
        self.Fly = Fly
        self.Water = Water
        self.Superplasticizer = Superplasticizer
        self.Coarse = Coarse
        self.Fine = Fine
        self.Age = Age

    def predict(self,features:pd.DataFrame):

        self.prediction_config = PredictionConfig()

        preprocessor = load_obj(self.prediction_config.preprocessor_path)
        model = load_obj(self.prediction_config.model_path)

        x = preprocessor.transform(features)
        y = model.predict(x)

        return y
    
    def get_data_as_dataframe(self):
        
        df = pd.DataFrame({"Cement":[self.Cement], "Blast":[self.Blast], "Fly":[self.Fly], "Water":[self.Water], 
              "Superplasticizer":[self.Superplasticizer], "Coarse":[self.Coarse], "Fine":[self.Fine], "Age":[self.Age]})
        
        return df
        

class BatchPrediction:
    def __init__(self,request: request):
        self.request = request
        self.prediction_config = PredictionConfig()

    def save_file(self):
        try:
            logging.info("Input file fetching and saving starts")

            input_file = self.request.files["file"]
            input_file_path = os.makedirs(os.path.join("Test_file",input_file.filename),exist_ok=True)

            input_file.save(input_file_path)

            return input_file_path
        
        except Exception as e:
            logging.info("Error occurred in fetching and saving file")
            raise CustomException(e,sys)
    
    def predict_file(self, input_file_path:str):
        try:
            logging.info("Prediction of file starts")

            df = pd.read_csv(input_file_path)
            self.prediction_config = PredictionConfig()

            preprocessor = load_obj(self.prediction_config.preprocessor_path)
            model = load_obj(self.prediction_config.model_path)

            x = preprocessor.transform(df)
            y = model.predict(x)

            data = pd.DataFrame(np.c_[x,y],columns = df.columns)

            os.makedirs(self.prediction_config.prediction_file_path,exist_ok=True)
            data.to_csv(self.prediction_config.prediction_file_path,header=True,index=False)

            return self.prediction_config.prediction_file_path
        
        except Exception as e:
            logging.info("Error occurred in predicted file saving")
            raise CustomException(e,sys)