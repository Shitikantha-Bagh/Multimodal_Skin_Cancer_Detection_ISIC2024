import os
import sys
import pandas as pd
import h5py

from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from kaggle.api.kaggle_api_extended import KaggleApi


@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', "train-metadata.csv")
    test_data_path: str = os.path.join('artifacts', "test-metadata.csv")
    train_image_path: str = os.path.join('artifacts', "train-image.hdf5")
    test_image_path: str = os.path.join('artifacts', "test-image.hdf5")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
        self.api = KaggleApi()
        self.api.authenticate()  

    def download_kaggle_data(self):
        logging.info("Downloading the dataset")
        try:
            os.makedirs('artifacts', exist_ok=True)
            
            # Downloading the files using Kaggle API
            self.api.competition_download_file('isic-2024-challenge', 'train-image.hdf5', path='artifacts')
            self.api.competition_download_file('isic-2024-challenge', 'test-image.hdf5', path='artifacts')
            self.api.competition_download_file('isic-2024-challenge', 'train-metadata.csv', path='artifacts')
            self.api.competition_download_file('isic-2024-challenge', 'test-metadata.csv', path='artifacts')

            logging.info("Data downloaded successfully!")
        except Exception as e:
            raise CustomException(e,sys)
        
    def load_data(self):
        logging.info("Loading data")
        try:
            train_df = pd.read_csv(self.ingestion_config.train_data_path).ffill()
            test_df = pd.read_csv(self.ingestion_config.test_data_path).ffill()

            train_images = h5py.File(self.ingestion_config.train_image_path, 'r')
            test_images = h5py.File(self.ingestion_config.test_image_path, 'r')

            return train_df, test_df, train_images, test_images

        except Exception as e:
            raise CustomException(e,sys)
        
if __name__ == "__main__":
    data_ingestion = DataIngestion()
    data_ingestion.download_kaggle_data()
    train_df, test_df, train_images, test_images = data_ingestion.load_data()