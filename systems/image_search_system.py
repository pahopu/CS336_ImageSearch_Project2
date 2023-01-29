import time
import cv2 as cv
import numpy as np
import feature_extractor as fe

from PIL import Image
from tqdm import tqdm
from pathlib import Path
from pickle import dump, load
from scipy.spatial.distance import cosine


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

        # Create datasets folder path --> contains dataset
        # If not exist, create a new folder
        self.datasets_folder_path = Path('datasets') / dataset_name
        if not self.datasets_folder_path.exists():
            self.datasets_folder_path.mkdir()

        # Create images folder path --> contains images of dataset
        # If not exist, create a new folder
        self.images_folder_path = self.datasets_folder_path / 'images'
        if not self.images_folder_path.exists():
            self.images_folder_path.mkdir()

        # Create binary folder path --> contains binary files about features and image paths
        # If not exist, create a new folder
        self.binary_folder_path = self.datasets_folder_path / 'binary'
        if not self.binary_folder_path.exists():
            self.binary_folder_path.mkdir()

        # Create methods folder path --> contains binary files of corresponding feature extractor
        # If not exist, create a new folder
        self.methods_folder_path = self.binary_folder_path / self.method
        if not self.methods_folder_path.exists():
            self.methods_folder_path.mkdir()

        # Create ground truth folder path --> contains files for evaluating
        # If not exist, create a new folder
        self.groundtruth_folder_path = self.datasets_folder_path / 'groundtruth'
        if not self.groundtruth_folder_path.exists():
            self.groundtruth_folder_path.mkdir()

    def indexing(self) -> None:
        # Create features file path and image paths file path
        # If not exist, create new files
        features_file_path = self.methods_folder_path / 'features.pkl'
        image_paths_file_path = self.methods_folder_path / 'images.pkl'

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

    def retrieve_image(self, query_image, K=16) -> tuple:
        # Start counting time
        start = time.time()

        # Get features file path and image paths file path
        features_file_path = self.methods_folder_path / 'features.pkl'
        image_paths_file_path = self.methods_folder_path / 'images.pkl'

        # Open features file and image paths file to read
        features_file = open(features_file_path, 'rb')
        image_paths_file = open(image_paths_file_path, 'rb')

        # Load features list and image paths list from the respective opened files
        features = load(features_file)
        image_paths = load(image_paths_file)

        if isinstance(query_image, str):  # If query image is a path (string type)
            query_image = Image.open(query_image)  # Open query image at image path
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

    def retrieve_image_and_print(self, query_image, K=16) -> None:
        # Retrieve image and get result, query time
        rel_imgs, query_time = self.retrieve_image(query_image, K)

        # Assign name of query image is None
        query_image_name = None

        if isinstance(query_image, str):  # If query image is a path (string type)
            query_image_name = Path(query_image).stem # Assign name of query image based on path
            query_image = cv.imread(query_image)  # Open query image with OpenCV

        if isinstance(query_image, Image.Image): # If query image is a subclass of Image
            # If name of query image is None, assign to 'No name'
            # Else keep the saved name
            query_image_name = 'No name' if query_image_name is None else query_image_name
            query_image = np.array(query_image) # Convert query image to np.array

        # Display query image and wait until close image
        cv.imshow(f'Query Image name: {query_image_name}', query_image)
        cv.waitKey(0)

        # Print name of query image
        print('\n' + '-' * 12 + ' RETRIEVE IMAGE ' + '-' * 13)
        print(f'Query Image name: {query_image_name}')

        # Print name and rank of relevant images
        print('-' * 10 + f' {K:3d} RELEVANT IMAGES ' + '-' * 10)

        # Browse each image in relevant images
        for id, (image, score) in enumerate(rel_imgs):
            # Open image from image path
            rel_img = cv.imread(str(image))

            # Display image
            cv.imshow(f'Relevant Image {id + 1}: {image.stem}', rel_img)

            # Print rank and name of image
            print(f'{(id + 1):3d}. {image.stem}')

            # Wait until close image
            cv.waitKey(0)

        print('-' * 41)

        # Print query time
        print(f'Query Time = {query_time:2.2f} seconds.\n')


if __name__ == '__main__':
    # Name of dataset and method
    dataset_name = 'oxbuild'
    method = 'Xception'

    # Create Image Search System object
    IS = ImageSearch_System(dataset_name, method)

    # Retrieve and print relevant images based on query image path or query image
    query_image_path = 'datasets/oxbuild/images/all_souls_000000.jpg' # Query image path
    query_image = Image.open(query_image_path) # Query image

    IS.retrieve_image_and_print(query_image_path) # Retrieve and print results