import cv2
import pytesseract
import numpy as np
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
    # Read the image
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Grayscale Image', gray)

    # Binarize the image (thresholding)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow('Binarized Image', binary)

    # Optional: Denoise or blur the image if needed
    blurred = cv2.GaussianBlur(binary, (5, 5), 0)
    cv2.imshow('Blurred Image', blurred)

    # Show images for debugging purposes
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return blurred


def extract_text(image):
    # OCR the image using Tesseract
    text = pytesseract.image_to_string(image)
    return text


def summarize_receipt(text):
    # Example of basic parsing logic (can be expanded)
    lines = text.split("\n")
    items = []
    subtotal = 0
    for line in lines:
        if line.startswith("#"):  # Item line starts with #
            item_data = line.split("\t")  # Example: item name, quantity, price
            items.append(item_data)
        if "Sub Total" in line:
            subtotal = float(line.split()[-1])

    summary = {
        "items": items,
        "subtotal": subtotal,
    }
    return summary


def main(image_path):
    # Process the image
    processed_image = preprocess_image(image_path)

    # Extract text
    text = extract_text(processed_image)
    print("Extracted Text:\n", text)

    # Summarize the receipt
    summary = summarize_receipt(text)
    print("\nReceipt Summary:")
    print("Subtotal:", summary['subtotal'])


if __name__ == "__main__":
    image_path = 'Recept-I.png'
    main(image_path)