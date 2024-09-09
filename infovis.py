
import os
import ast

# Function to get the absolute path of a file based on the script's location
def get_file_path(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, filename)


# Function to validate if the summary data is in the correct format
def validate_summary_data(summary):
    if not isinstance(summary, dict):
        raise ValueError("Expected the summary data to be a dictionary.")
    if "items" not in summary:
        raise ValueError("Missing 'items' key in summary data.")
    if not isinstance(summary["items"], list):
        raise ValueError("The 'items' key should hold a list.")
    for item in summary["items"]:
        if not all(key in item for key in ("name", "price")):
            raise ValueError("Each item needs to have both 'name' and 'price'.")
