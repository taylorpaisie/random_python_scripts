#!/bin/env python
# this script will copy from a list in text file format to the directory of your choosing

import shutil
import os, sys

# Path to the text file containing the list of file paths
file_list_path = sys.argv[1]

# Directory to copy the files to
destination_directory = sys.argv[2]

# Create the destination directory if it doesn't exist
os.makedirs(destination_directory, exist_ok=True)

# Read the file paths from the text file
with open(file_list_path, 'r') as file:
    file_paths = file.readlines()

# Copy each file to the destination directory
for file_path in file_paths:
    file_path = file_path.strip()  # Remove any leading/trailing whitespace
    if os.path.isfile(file_path):
        shutil.copy(file_path, destination_directory)
        print(f'Copied {file_path} to {destination_directory}')
    else:
        print(f'File not found: {file_path}')
