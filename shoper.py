import cv2
import pytesseract
import numpy as np
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# Preprocess the image (grayscale, binarization, etc.)
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )

    # Apply morphological operations to remove noise
    kernel = np.ones((2, 2), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    binary = cv2.dilate(binary, kernel, iterations=1)

    # Apply Gaussian Blur
    blurred = cv2.GaussianBlur(binary, (5, 5), 0)

    cv2.imshow('Grayscale Image', gray)
    cv2.imshow('Binarized Image', binary)
    cv2.imshow('Blurred Image', blurred)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return blurred

def extract_text(image):
    text = pytesseract.image_to_string(image)
    return text

def save_text_to_file(text, output_file):
    summary_folder = os.path.join(os.path.dirname(os.path.abspath(_file_)), "summary")
    os.makedirs(summary_folder, exist_ok=True)
    with open(os.path.join(summary_folder, output_file), "w") as file:
        file.write(text)
    print(f"Extracted text saved to {os.path.join(summary_folder, output_file)}")

def summarize_receipt(text):
    lines = text.split("\n")
    items = []
    subtotal = 0.0
    for line in lines:
        parts = line.split()
        if len(parts) >= 3 and parts[-1].replace('.', '', 1).isdigit():
            price = parts[-1]
            quantity = parts[-2]
            name = ' '.join(parts[:-2])
            items.append({
                "name": name.strip(),
                "price": price.strip()
            })
        elif "Sub Total" in line:
            try:
                subtotal = float(line.split()[-1])
            except ValueError:
                print(f"Unable to parse subtotal from line: {line}")

    summary = {
        "items": items,
        "subtotal": subtotal,
    }

    return summary

def save_summary_to_file(summary, output_file):
    summary_folder = os.path.join(os.path.dirname(os.path.abspath(_file_)), "summary")
    os.makedirs(summary_folder, exist_ok=True)
    with open(os.path.join(summary_folder, output_file), "w") as file:
        file.write(str(summary))
    print(f"Summary saved to {os.path.join(summary_folder, output_file)}")


# Main function to process the receipt and save both text and summary
def main(image_path):
    # Process the image
    processed_image = preprocess_image(image_path)

    # Extract text
    text = extract_text(processed_image)
    print("Extracted Text:\n", text) 

    # Save the extracted text
    save_text_to_file(text, "receipt_text.txt")

    # Summarize the receipt and save the summary
    summary = summarize_receipt(text)
    save_summary_to_file(summary, "receipt_summary.txt")

if _name_ == "_main_":
    image_path = 'Recept-II.png'
    main(image_path)