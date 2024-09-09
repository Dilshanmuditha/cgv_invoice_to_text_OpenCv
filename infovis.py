import matplotlib.pyplot as plt
import os
import ast

# Function to get the absolute path of a file
def get_file_path(filename):
    current_dir = os.path.dirname(os.path.abspath(_file_))
    return os.path.join(current_dir, filename)

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

def visualize_sales(summary):
    validate_summary_data(summary)
    item_names = [item["name"] for item in summary["items"]]
    item_prices = [float(item["price"]) for item in summary["items"]]

    if not item_names or not item_prices:
        print("No items found in the summary. Skipping visualization.")
        return

    plt.figure(figsize=(10, 6))
    plt.bar(item_names, item_prices, color='blue')
    plt.xlabel('Items')
    plt.ylabel('Prices (Currency)')
    plt.title('Sales Summary')
    plt.xticks(rotation=45, ha="right")

    # Save the graph to a file
    graph_folder = os.path.join(os.path.dirname(os.path.abspath(_file_)), "visualization")
    os.makedirs(graph_folder, exist_ok=True)
    plt.savefig(os.path.join(graph_folder, "sales_summary.png"))
    plt.show()

def main():
    summary_file_path = get_file_path(os.path.join("summary", "receipt_summary.txt"))

    if not os.path.exists(summary_file_path):
        raise FileNotFoundError(f"Cannot find the file {summary_file_path}. Please ensure the summary is generated.")

    with open(summary_file_path, "r") as file:
        try:
            summary = ast.literal_eval(file.read())
        except (SyntaxError, ValueError) as e:
            raise ValueError("Error parsing the summary file. Ensure it is in valid dictionary format.") from e

    print("Loaded Summary:", summary)

    # Generate the sales visualization
    visualize_sales(summary)


if _name_ == "_main_":
    main()