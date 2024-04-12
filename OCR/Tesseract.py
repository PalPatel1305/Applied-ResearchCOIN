"""
This script performs OCR (Optical Character Recognition) on a directory of PDF files,
extracting text from each page and saving the results to a JSON file.

Dependencies:
    - pytesseract (https://pypi.org/project/pytesseract/): For OCR (Optical Character Recognition).
    - json (https://docs.python.org/3/library/json.html): For JSON file operations.
    - os (https://docs.python.org/3/library/os.html): For operating system related functionalities.
    - pdf2image (https://pypi.org/project/pdf2image/): For converting PDF to images.

Usage:
    - Ensure the required dependencies are installed.
    - Update the path to the Tesseract executable using the variable `pytesseract.pytesseract.tesseract_cmd`.
    - Update the paths for the PDF directory (`pdf_directory`) and output directory (`output_directory`).
    - Run the script to perform OCR on the PDF files in the specified directory.
    
Output:
    - The script saves the OCR results to a JSON file.
    - The JSON file contains the extracted text from each page of the PDF files, organized by month.
    - Each month's data is represented as a dictionary, where the keys are the page numbers and the values are the OCR text.
    - The JSON file structure allows easy access to the OCR text for each page of each month's PDF files.

"""
# Import necessary libraries
import pytesseract  # For OCR (Optical Character Recognition)
import json  # For JSON file operations
import os  # For operating system related functionalities
from pdf2image import convert_from_path  # For converting PDF to images

# Update the path to the Tesseract executable based on your installation
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Directory with your PDF files
pdf_directory = r'journals'

# Output directory for OCR results
output_directory = r'FullJournalPageData'

# Ensure the output directory exists, if not, create it
os.makedirs(output_directory, exist_ok=True)

# Main dictionary for OCR results, keyed by month numbers
ocr_results_by_month = {}

# Global page counter for continuous numbering
global_page_counter = 1

# Process each PDF file in the directory
for filename in sorted(os.listdir(pdf_directory)):
    if filename.endswith('.pdf'):
        # Extracting the month number directly from the filename
        month_number = filename.split('N')[2][:2]  # This will extract the two-digit month number

        pdf_path = os.path.join(pdf_directory, filename)
        images = convert_from_path(pdf_path, dpi=300)  # Convert PDF to images

        for image in images:
            # Perform OCR on each image
            ocr_text = pytesseract.image_to_string(image)

            # Store OCR results in the dictionary
            if month_number not in ocr_results_by_month:
                ocr_results_by_month[month_number] = {}
            ocr_results_by_month[month_number][f'{global_page_counter}'] = ocr_text

            # Increment global page counter for continuous numbering
            global_page_counter += 1  

# Output JSON file path
output_json_path = os.path.join(output_directory, 'FullJournalData.json')

# Write OCR results to JSON file
with open(output_json_path, 'w') as json_file:
    json.dump(ocr_results_by_month, json_file, indent=2)

# Print confirmation message
print("OCR results saved to", output_json_path)
