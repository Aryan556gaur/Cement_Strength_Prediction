import os, sys
from src.logger import logging
from src.exception import CustomException
from src.utils import save_object, read_yaml
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score
from dataclasses import dataclass

@dataclass
class ModelTrainerConfig:
    model_path = os.path.join("artifacts","model.pkl")
    yaml_file_path = os.path.join("config","model.yaml")

class ModelTrainer:
    def __init__(self):
        self.trainer_config = ModelTrainerConfig()

    def initiate_training(self,x_train,x_test,y_train,y_test):

        try:
            logging.info("Model Training Starts")

            models = {"RandomForestRegressor": RandomForestRegressor(),
            "XGBRegressor": XGBRegressor(),"GradientBoostingRegressor": GradientBoostingRegressor(),
            "DecisionTreeRegressor": DecisionTreeRegressor(),"SVR": SVR()}

            model_param = {}
            model_score = {}
            for i in range(len(models)):
                model = list(models.values())[i]
                grid = GridSearchCV(model,param_grid = read_yaml(self.trainer_config.yaml_file_path)["model_selection"]["model"][list(models.keys())[i]]['search_param_grid'],cv=5,error_score="raise")
                grid.fit(x_train,y_train)
                pred = grid.predict(x_test)
                score = r2_score(y_test,pred)
                parameters = grid.best_params_

                model_param[list(models.keys())[i]] = parameters
                model_score[list(models.keys())[i]] = score

            best_model_name = list(model_score.keys())[list(model_score.values()).index(max(list(model_score.values())))]
            best_model_parameters = model_param[best_model_name]
            best_model_obj = models[best_model_name]

            final_model = best_model_obj.set_params(**best_model_parameters)

            save_object(self.trainer_config.model_path,final_model)

            logging.info("Model Training successful")
        
        except Exception as e:
            logging.info("Error occurred in Model Training")
            raise CustomException(e,sys)
