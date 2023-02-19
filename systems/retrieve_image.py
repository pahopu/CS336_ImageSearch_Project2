from image_search_system import ImageSearch_System as ISS

if __name__ == '__main__':
    # Name of dataset and method
    dataset_name = 'oxbuild'
    method = 'Xception'

    # Create Image Search System object
    IS = ISS(dataset_name, method)

    # Create image path, retrieve and print result
    image_path = 'static/datasets/oxbuild/images/all_souls_000000.jpg'
    IS.retrieve_image_and_print(image_path)