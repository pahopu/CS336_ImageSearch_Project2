import time
import cv2 as cv
import numpy as np

from PIL import Image
from tqdm import tqdm
from pathlib import Path
from pickle import dump, load
from scipy.spatial.distance import cosine

try:
    import feature_extractor as fe
except:
    import systems.feature_extractor as fe


class ImageSearch_System:
    def __init__(self, dataset_name='oxbuild', method='VGG16') -> None:
        # Select feature extractor based on corresponding method
        if method == 'VGG16':
            self.feature_extractor = fe.VGG16_FE()
        elif method == 'Xception':
            self.feature_extractor = fe.Xception_FE()
        elif method == 'InceptionV3':
            self.feature_extractor = fe.InceptionV3_FE()
        elif method == 'ResNet152V2':
            self.feature_extractor = fe.ResNet152V2_FE()
        elif method == 'EfficientNetV2L':
            self.feature_extractor = fe.EfficientNetV2L_FE()
        elif method == 'InceptionResNetV2':
            self.feature_extractor = fe.InceptionResNetV2_FE()

        # Save method name
        self.method = method

        # Create datasets folder path --> contains dataset
        # If not exist, create a new folder
        self.dataset_folder_path = Path('datasets') / dataset_name
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

        # Create methods folder path --> contains binary files of corresponding feature extractor
        # If not exist, create a new folder
        self.methods_folder_path = self.binary_folder_path / self.method
        if not self.methods_folder_path.exists():
            self.methods_folder_path.mkdir()

        # Create ground truth folder path --> contains files for evaluating
        # If not exist, create a new folder
        self.groundtruth_folder_path = self.dataset_folder_path / 'groundtruth'
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
                # Image processing and saving
                # If error, move to next image
                try:
                    # Open image at image path
                    image = Image.open(image_path)

                    # Extract feature from image
                    feature = self.feature_extractor.extract(image)

                    # Add feature to features list, image path to image paths list
                    features.append(feature)
                    image_paths.append(image_path)
                except:
                    continue

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
            query_image_name = Path(query_image).stem  # Assign name of query image based on path
            query_image = cv.imread(query_image)  # Open query image with OpenCV

        if isinstance(query_image, Image.Image):  # If query image is a subclass of Image
            # If name of query image is None, assign to 'No name'
            # Else keep the saved name
            query_image_name = 'No name' if query_image_name is None else query_image_name
            query_image = np.array(query_image)  # Convert query image to np.array

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

    def AP(self, predict, groundtruth, interpolated=False):
        # Create precision, recall list
        p = []
        r = []
        correct = 0  # Number of correct images

        # Browse each image in predict list
        for id, (image, score) in enumerate(predict):
            # If image in groundtruth
            if image.stem in groundtruth:
                correct += 1  # Increase number of correct images
                p.append(correct / (id + 1))  # Add precision at this position
                if interpolated:  # If interpolated AP
                    r.append(correct / len(groundtruth))  # Add recall at this position

        if interpolated:  # If call interpolated AP
            trec = []  # Calculate precision at 11 point of TREC
            for R in range(11):  # Browse 11 point of recall from 0 to 1 with step 0.1
                pm = []  # Create precision list to find max precision
                for id, pr in enumerate(p):  # Browse each precision above
                    if r[id] >= R / 10:  # If corresponding recall is greater than or equal to this point
                        pm.append(pr)  # Add precision to precision list to find max
                trec.append(max(pm) if len(pm) else 0)  # Add max precision at this point to trec
            return np.mean(np.array(trec)) if len(trec) else 0  # Return interpolated AP

        return np.mean(np.array(p)) if len(p) else 0  # Return non - interpolated AP

    def evaluating(self):
        # Create results folder path --> contains result file of evaluating
        # If not exist, create a new folder
        results_folder_path = self.dataset_folder_path / 'results'
        if not results_folder_path.exists():
            results_folder_path.mkdir()

        # Create result file path --> save result of evaluating
        # If exist, remove file
        result_file_path = results_folder_path / f'{self.dataset_folder_path.stem}_{self.method}_evaluation.txt'
        if result_file_path.exists():
            result_file_path.unlink()

        # Open result file at result file path to write
        result_file = open(result_file_path, 'a')

        # Write header line
        result_file.write('-' * 20 + 'START EVALUATING' + '-' * 20 + '\n\n')

        # Start counting time of evaluating
        start = time.time()

        # Get query files from groundtruth folder path
        queries_file = sorted(self.groundtruth_folder_path.glob('*_query.txt'))

        # Create list to save non - interpolated and interpolated APs
        nAPs = []
        iAPs = []

        # Browse each query file in queries file
        for id, query_file in enumerate(queries_file):
            # Create groundtruth list
            groundtruth = []

            # Get groundtruth from file with 'good' result
            with open(str(query_file).replace('query', 'good'), 'r') as groundtruth_file:
                groundtruth.extend([line.strip() for line in groundtruth_file.readlines()])

            # Get groundtruth from file with 'ok' result            
            with open(str(query_file).replace('query', 'ok'), 'r') as groundtruth_file:
                groundtruth.extend([line.strip() for line in groundtruth_file.readlines()])

            # Get length of groundtruth
            G = len(groundtruth)

            # Open query file to read
            with open(query_file, 'r') as query:
                # Get content of query file
                content = query.readline().strip().split()

                # Get string need to replace
                if self.dataset_folder_path.stem == 'oxbuild':
                    replace_str = 'oxc1_'
                elif self.dataset_folder_path.stem == 'paris':
                    replace_str = ''

                # Get image path and coordinates of bounding box
                image_name = content[0].replace(replace_str, '') + '.jpg'
                image_path = self.images_folder_path / image_name
                bounding_box = tuple(float(coor) for coor in content[1:])

                # Open query image and crop image based on bounding box
                query_image = Image.open(image_path)
                query_image = query_image.crop(bounding_box)

                # Retrieve image and get relevant images, query time
                rel_imgs, query_time = self.retrieve_image(query_image, G)

                # Calculate non - interpolated and interpolated AP
                nAP = self.AP(rel_imgs, groundtruth, interpolated=False)
                iAP = self.AP(rel_imgs, groundtruth, interpolated=True)

                # Add the AP values to the corresponding AP list
                nAPs.append(nAP)
                iAPs.append(iAP)

            # Write id and name of query file
            result_file.write(f'+ Query {(id + 1):2d}: {Path(query_file).stem}.txt\n')

            # Write non - interpolated and interpolated AP
            result_file.write(' ' * 12 + f'Non - Interpolated Average Precision = {nAP:.2f}\n')
            result_file.write(' ' * 12 + f'Interpolated Average Precision = {iAP:.2f}\n')

            # Write query time
            result_file.write(' ' * 12 + f'Query Time = {query_time:2.2f}s\n')

        # End counting time of evaluating
        end = time.time()

        # Write footer line
        result_file.write('\n' + '-' * 19 + 'FINISH EVALUATING' + '-' * 20 + '\n\n')

        # Calculate non - interpolated and interpolated MAP
        nMAP = np.mean(np.array(nAPs))
        iMAP = np.mean(np.array(iAPs))

        # Write total number of queries
        result_file.write(f'Total number of queries = {len(queries_file)}\n')

        # Write non - interpolated and interpolated MAP
        result_file.write(f'Non - Interpolated Mean Average Precision = {nMAP:.2f}\n')
        result_file.write(f'Interpolated Mean Average Precision = {iMAP:.2f}\n')

        # Write evaluating time
        result_file.write(f'Evaluating Time = {(end - start):2.2f}s')

        # Close result file
        result_file.close()