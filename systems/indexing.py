from image_search_system import ImageSearch_System as ISS

if __name__ == '__main__':
    # Name of dataset
    dataset_name = 'oxbuild'

    # Create Image Search System object
    IS = ISS(dataset_name)

    # Extract all features
    IS.indexing()