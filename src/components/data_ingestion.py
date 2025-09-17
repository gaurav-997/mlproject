import os
import sys
from src.exception import CustomException
from src.logger import logging
from sklearn.model_selection import train_test_split
import pandas as pd
from dataclasses import dataclass
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

#  providing inputs required for dataingestion 
@dataclass
class DataIngestionConfig:
    train_data_path:str = os.path.join('artifacts',"train.csv") # here it shows artifact dir has train.csv file 
    test_data_path:str = os.path.join('artifacts',"test.csv")
    raw_data_path:str = os.path.join('artifacts',"raw.csv")
    
class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            df = pd.read_csv("notebook/stud.csv")
            logging.info("read the data as dataframe")
        
            #  creating artifacts directory 
            dir_path = os.path.dirname(self.data_ingestion_config.train_data_path)
            os.makedirs(dir_path,exist_ok=True)
            
            logging.info("conveting data frame to csv format ")
            df.to_csv(self.data_ingestion_config.raw_data_path,index=False,header= True)
            
            logging.info("train test split initiate , spliting the data frame into train & test sets")
            train_set,test_set = train_test_split(df,test_size=0.2,random_state=42)
            
            train_set.to_csv(self.data_ingestion_config.train_data_path,index=False,header= True)
            test_set.to_csv(self.data_ingestion_config.test_data_path,index=False,header= True)
            
            logging.info("initiation of data is completed")
            
            return(
                self.data_ingestion_config.train_data_path,
                self.data_ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)

if __name__ == "__main__":
    obj = DataIngestion()
    train_data,test_data = obj.initiate_data_ingestion()
    data_transformation= DataTransformation()
    train_array,test_array,_ = data_transformation.initiate_data_transformation(train_data,test_data)
    model_trainer = ModelTrainer()
    model_trainer.initate_model_trainer(train_array,test_array)