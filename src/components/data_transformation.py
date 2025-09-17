import os
import sys
from src.exception import CustomException
from src.logger import logging
import numpy as np
import pandas as pd
from dataclasses import dataclass
from sklearn.compose import ColumnTransformer 
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
# from src.components.data_ingestion import DataIngestionConfig
#  columntransformer is used to create pipeline , Imputer used to handle missing values
from src.utils import save_object

#  providing inputs required for datatrasformation ( after transformation model is saved as preprocessor.pkl )
@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path:str = os.path.join('artifacts','preprocessor.pkl')
    
class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
        
    def get_transformer_object(self):
        logging.info("Entered the data transformation method or component")
        try:
            numerical_columns = ["reading_score","writing_score"]
            categorical_columns= ["gender","race_ethnicity","parental_level_of_education","lunch","test_preparation_course"]
            
            
            #  create numerical pipeline and handle missing values
            numerical_pipeline = Pipeline(steps=[
                ("imputer",SimpleImputer(strategy="median")),
                ("scaler",StandardScaler())
            ])
            
            #  create categorical pipeline and handle missing values ( replacing them with mode )
            categorical_pipeline = Pipeline(steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder()),
                ("scaler",StandardScaler(with_mean=False))
            ])
            
            logging.info(f"Numerical  columns standard scaling {numerical_columns} and  categorical columns encoding {categorical_columns} is completed ")
            #  combining numerical and categorical pipelines 
            preprocessor=ColumnTransformer(
                [
                ("num_pipeline",numerical_pipeline,numerical_columns),
                ("cat_pipelines",categorical_pipeline,categorical_columns)

                ]


            )
            return preprocessor
            
            
        except Exception as e:
            raise CustomException(e,sys)
        
        
    def initiate_data_transformation(self,train_data,test_data):
        try:
            logging.info("reading test and train data")
            train_df = pd.read_csv(train_data)
            test_df = pd.read_csv(test_data)
            
            logging.info('getting preporcessor obj ')
            preprocessor_object = self.get_transformer_object()
            
            target_column = "math_score"
            numerical_columns = ["reading_score","writing_score"]
            
            #  getting the cleaned train and test data
            input_feture_train_df = train_df.drop(columns=["Unnamed: 8","Unnamed: 9","Unnamed: 10",target_column])
            target_feature_train_df = train_df[target_column]
            
            input_feture_test_df = test_df.drop(columns=["Unnamed: 8","Unnamed: 9","Unnamed: 10",target_column])
            target_feature_test_df = test_df[target_column]
            
            logging.info("applying preprocessing object on training and testing dataframes")
            input_feature_train_array = preprocessor_object.fit_transform(input_feture_train_df)
            input_feature_test_array = preprocessor_object.transform(input_feture_test_df)
            #  from where fit_transform and transform are comming and whats the use of these and whats the difference btw both of them 
            
            train_arr = np.c_[input_feature_train_array,np.array(target_feature_train_df)]
            #  what is this np.c_ and what we will get after concating the input array and target df 
            test_arr = np.c_[input_feature_test_array,np.array(target_feature_test_df)]
            
            logging.info("saving preprocessing object")
            
            save_object(
                obj = preprocessor_object,file_path=self.data_transformation_config.preprocessor_obj_file_path
                
            )
            
            return(train_arr,test_arr,self.data_transformation_config.preprocessor_obj_file_path)
            
        except Exception as e:
            raise CustomException(e,sys)
        
        