import time
import numpy as np
import feature_extractor as fe

from PIL import Image
from tqdm import tqdm
from pathlib import Path
from pickle import dump, load
from scipy.stats import cosine


class ImageSearch_System:
    def __init__(self, dataset_name='oxbuild', method='VGG16') -> None:
        # Select feature extractor based on corresponding method
        if method == 'VGG16':
            self.feature_extractor = fe.VGG16_FE()
        elif method == 'Xception':
            self.feature_extractor = fe.Xception_FE()
        elif method == 'EfficientNetV2L':
            self.feature_extractor = fe.EfficientNetV2L_FE()

        # Save method name
        self.method = method

        # Create dataset folder path --> contains dataset
        # If not exist, create a new folder
        self.dataset_folder_path = Path('dataset') / dataset_name
        if not self.dataset_folder_path.exists():
            self.dataset_folder_path.mkdir()

        # Create images folder path --> contains images of dataset
        # If not exist, create a new folder
        self.images_folder_path = self.dataset_folder_path / 'images'
        if not self.images_folder_path.exists():
            self.images_folder_path.mkdir()

        # Create binary folder path --> contains binary files about features and image paths
        # If not exist, create a new folder
        self.binary_folder_path = self.dataset_folder_path / 'binary'
        if not self.binary_folder_path.exists():
            self.binary_folder_path.mkdir()

        # Create method folder path --> contains binary files of corresponding feature extractor
        # If not exist, create a new folder
        self.method_folder_path = self.binary_folder_path / self.method
        if not self.method_folder_path.exists():
            self.method_folder_path.mkdir()

    def indexing(self) -> None:
        # Create features file path and image paths file path
        # If not exist, create new files
        features_file_path = self.method_folder_path / 'features.pkl'
        image_paths_file_path = self.method_folder_path / 'images.pkl'

        if not features_file_path.exists() and not image_paths_file_path.exists():
            # Create features list and image paths list
            features, image_paths = [], []

            # Browse each image at images folder path with suffix .jpg
            for image_path in tqdm(sorted(self.images_folder_path.glob('*.jpg'))):
                # Open image at image path
                image = Image.open(image_path)

                # Extract feature from image
                feature = self.feature_extractor.extract(image)

                # Add feature to features list, image path to image paths list
                features.append(feature)
                image_paths.append(image_path)

            # Open features file and image paths file to write
            features_file = open(features_file_path, 'wb')
            image_paths_file = open(image_paths_file_path, 'wb')

            # Save features list and image paths list to the respective opened files
            dump(features, features_file)
            dump(image_paths, image_paths_file)

    def retrieve_image(self, image_path, K=16) -> tuple:
        # Start counting time
        start = time.time()

        # Get features file path and image paths file path
        features_file_path = self.method_folder_path / 'features.pkl'
        image_paths_file_path = self.method_folder_path / 'images.pkl'

        # Open features file and image paths file to read
        features_file = open(features_file_path, 'rb')
        image_paths_file = open(image_paths_file_path, 'rb')

        # Load features list and image paths list from the respective opened files
        features = load(features_file)
        image_paths = load(image_paths_file)

        query_image = Image.open(image_path)  # Open query image at image path
        query_feature = self.feature_extractor.extract(query_image)  # Extract query feature from query image

        # Create scores list contains cosine similarity between 
        # Query feature and each feature in features list
        scores = []
        for feature in features:
            # Calculate consine similarity score
            score = 1 - cosine(query_feature, feature)
            scores.append(score)  # Add score to scores list

        # Get top K image ids with highest score
        topk_ids = np.argsort(scores)[::-1][:K]

        # Get image path with corresponding similarity from top K image ids
        ranked = [(image_paths[id], scores[id]) for id in topk_ids]

        # End counting time
        end = time.time()   

        # Return top K relevant images and query time
        return ranked, end - start


if __name__ == '__main__':
    IS = ImageSearch_System()
    IS.indexing()