from image_search_system import ImageSearch_System as ISS

if __name__ == '__main__':
    # Name of dataset and method
    dataset_name = 'oxbuild'
    method = 'Xception'

    # Create Image Search System object
    IS = ISS(dataset_name, method)

    # Extract all features
    IS.indexing()