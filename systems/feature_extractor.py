import numpy as np

from keras.models import Model
from keras.utils import img_to_array
from keras.applications import xception, vgg16, efficientnet_v2


class Xception_FE:
    def __init__(self) -> None:
        base_model = xception.Xception()  # Create Xception model

        # Create model based on Xception model above
        # With input is the same as Xception model
        # And output results from avg_pool layer of Xception model
        # (None, 299, 299, 3) --> (None, 2048)
        self.model = Model(inputs=base_model.input, outputs=base_model.get_layer('avg_pool').output)

    def extract(self, image) -> np.ndarray:
        image = image.resize((299, 299))  # Image must be 299 x 299 pixels
        image = image.convert('RGB')  # Image must be color photo

        array = img_to_array(image)  # Image to np.array with shape (299, 299, 3)
        array = np.expand_dims(array, axis=0)  # (299, 299, 3) --> (1, 299, 299, 3)
        array = xception.preprocess_input(array)  # Subtracting average values for each pixel

        feature = self.model.predict(array)[0]  # Predict with shape (1, 2048) --> (2048, )
        feature = feature / np.linalg.norm(feature)  # Normalize

        return feature


class EfficientNetV2L_FE:
    def __init__(self) -> None:
        base_model = efficientnet_v2.EfficientNetV2L()  # Create EfficientNetV2L model

        # Create model based on EfficientNetV2L model above
        # With input is the same as EfficientNetV2L model
        # And output results from top_dropout layer of EfficientNetV2L model
        # (None, 480, 480, 3) --> (None, 1280)
        self.model = Model(inputs=base_model.input, outputs=base_model.get_layer('top_dropout').output)

    def extract(self, image) -> np.ndarray:
        image = image.resize((480, 480))  # Image must be 480 x 480 pixels
        image = image.convert('RGB')  # Image must be color photo

        array = img_to_array(image)  # Image to np.array with shape (480, 480, 3)
        array = np.expand_dims(array, axis=0)  # (480, 480, 3) --> (1, 480, 480, 3)
        array = efficientnet_v2.preprocess_input(array)  # Subtracting average values for each pixel

        feature = self.model.predict(array)[0]  # Predict with shape (1, 1280) --> (1280, )
        feature = feature / np.linalg.norm(feature)  # Normalize

        return feature


class VGG16_FE:
    def __init__(self) -> None:
        base_model = vgg16.VGG16()  # Create VGG16 model

        # Create model based on VGG16 model above
        # With input is the same as VGG16 model
        # And output results from fc1 layer of VGG16 model
        # (None, 224, 224, 3) --> (None, 4096)
        self.model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)

    def extract(self, image) -> np.ndarray:
        image = image.resize((224, 224))  # Image must be 224 x 224 pixels
        image = image.convert('RGB')  # Image must be color photo

        array = img_to_array(image)  # Image to np.array with shape (224, 224, 3)
        array = np.expand_dims(array, axis=0)  # (224, 224, 3) --> (1, 224, 224, 3)
        array = vgg16.preprocess_input(array)  # Subtracting average values for each pixel

        feature = self.model.predict(array)[0]  # Predict with shape (1, 4096) --> (4096, )
        feature = feature / np.linalg.norm(feature)  # Normalize feature

        return feature
