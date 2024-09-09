
import os
import ast

# Function to get the absolute path of a file based on the script's location
def get_file_path(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, filename)
