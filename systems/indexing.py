import argparse

from image_search_system import ImageSearch_System as ISS

if __name__ == '__main__':
    # Create parser and add arguments
    argParser = argparse.ArgumentParser()
    argParser.add_argument('-d', '--dataset', help='Name of dataset')
    argParser.add_argument('-m', '--method', help='Name of method')

    # Create arguments
    args = argParser.parse_args()

    # Create Image Search System object
    IS = ISS(args.dataset, args.method)

    # Extract all features
    IS.indexing()