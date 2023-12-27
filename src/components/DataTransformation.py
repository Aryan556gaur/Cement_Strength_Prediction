import os, sys
import pandas as pd
from src.logger import logging
from src.exception import CustomException
from src.utils import save_object
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from dataclasses import dataclass

@dataclass
class DataTransformationConfig:
    preprocessor_path = os.path.join("artifacts","preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.transformation_Config = DataTransformationConfig()

    def preprocessing(self):
        preprocessor = Pipeline(
            steps=(
                ("imputer",KNNImputer(n_neighbors=5)),
                ("scaler",StandardScaler())
            )
        )
        return preprocessor
        

    def initiate_Transformation(self,Raw_data_path):

        try:
            logging.info("Data transformation starts")

            df = pd.read_csv(Raw_data_path)

            new_columns = [c.split()[0] for c in df.columns]
            df = df.rename(columns=dict(zip(df.columns, new_columns)))

            Q1 = df.quantile(0.25)
            Q3 = df.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df = df[(df >= lower_bound) & (df <= upper_bound)]

            df.drop_duplicates(inplace=True)
            df.reset_index(inplace=True)
            df.drop("index",axis=1,inplace=True)

            x = df.drop("Concrete",axis=1)
            y = df["Concrete"]

            x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.25,random_state=42)

            preprocessor = self.preprocessing()
            x_train = preprocessor.fit_transform(x_train)
            x_test = preprocessor.transform(x_test)

            save_object(self.transformation_Config.preprocessor_path,preprocessor)

            logging.info("Data Transformation Completed")

            return x_train,x_test,y_train,y_test

        
        except Exception as e:
            logging.info("Exception occured in Data Transformation")
            raise CustomException(e,sys)