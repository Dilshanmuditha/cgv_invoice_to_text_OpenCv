
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

# Main function to read summary data and visualize it
def main():
    summary_file_path = get_file_path(os.path.join("summary", "receipt_summary.txt"))

    if not os.path.exists(summary_file_path):
        raise FileNotFoundError(f"Cannot find the file {summary_file_path}. Please ensure the summary is generated.")

    # Load and parse the summary data
    with open(summary_file_path, "r") as file:
        try:
            summary = ast.literal_eval(file.read())  # Safely interpret the file contents as a dictionary
        except (SyntaxError, ValueError) as e:
            raise ValueError("Error parsing the summary file. Ensure it is in valid dictionary format.") from e

    # Generate the sales visualization
    visualize_sales(summary)


# Entry point of the program
if __name__ == "__main__":
    main()
