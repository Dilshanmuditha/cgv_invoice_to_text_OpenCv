import cv2
import pytesseract
import numpy as np
import matplotlib.pyplot as plt
import sys

# Path to Tesseract executable (update if different)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def show_progress(step):
    print(f"[INFO] {step}...")


def preprocess_image(image_path):
    # Read the image
    show_progress("Reading the image")
    img = cv2.imread(image_path)

    # Convert to grayscale
    show_progress("Converting to grayscale")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Binarize the image (thresholding)
    show_progress("Binarizing the image")
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Optional: Denoise or blur the image if needed
    show_progress("Applying Gaussian Blur")
    blurred = cv2.GaussianBlur(binary, (5, 5), 0)

    show_progress("Image preprocessing completed")
    return blurred


def extract_text(image):
    # OCR the image using Tesseract
    show_progress("Extracting text using OCR")
    text = pytesseract.image_to_string(image)
    return text


def parse_receipt(text):
    show_progress("Parsing receipt data")
    lines = text.split("\n")
    items = {}

    for line in lines:
        line = line.strip()
        if line.startswith("#"):  # Assuming each item starts with '#'
            try:
                parts = line.split("\t")  # Split into name, quantity, price
                item_name = parts[0][1:]  # Remove '#' from item name
                quantity = float(parts[1])
                price = float(parts[2])
                items[item_name] = price * quantity
            except (IndexError, ValueError):
                continue  # Ignore lines that don't match format

    return items


def visualize_sales(sales_data):
    show_progress("Visualizing sales summary")

    if not sales_data:
        print("[ERROR] No sales data to visualize.")
        return

    # Extract item names and sales amounts
    item_names = list(sales_data.keys())
    sales_amounts = list(sales_data.values())

    # Plot a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(item_names, sales_amounts, color='skyblue')

    # Add labels and title
    plt.xlabel("Item")
    plt.ylabel("Total Sales ($)")
    plt.title("Sales Summary by Item")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Show the plot
    plt.show()


def main(image_path):
    print("[INFO] Starting receipt processing...")

    # Process the image
    processed_image = preprocess_image(image_path)

    # Extract text
    text = extract_text(processed_image)
    print("\nExtracted Text:\n", text)

    # Parse receipt for sales data
    sales_data = parse_receipt(text)

    # Visualize the sales summary
    visualize_sales(sales_data)

    print("[INFO] Processing complete!")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python infovis.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    main(image_path)
