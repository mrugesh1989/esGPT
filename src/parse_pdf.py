import os
import PyPDF2
from PyPDF2 import PdfReader
from google.cloud import storage
import io

def read_bytes_pdf(file_bytes):
   # Create a file-like object from the bytes
    file_object = io.BytesIO(file_bytes)

    # Create a PDF file reader
    pdf_file_reader = PdfReader(file_object)

    # Initialize an empty string to hold the text
    text = ''

    # Loop through each page in the PDF file
    for page in pdf_file_reader.pages:
        # Extract the text from the page
        text += page.extract_text()

    return text


# Read PDF file
def read_pdf(pdf_file):
    text = ""
    reader = PyPDF2.PdfReader(pdf_file)
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text


def read_pdfs_in_bucket(bucket_name, entity_name):
    """
    Function to read all PDF files in a specified Google Cloud Storage bucket and extract their text.
    """
    # Create a client
    client = storage.Client()

    # Get the bucket
    bucket = client.get_bucket(bucket_name)

    extracted_texts = {}
    blobs_found = False
    for blob in bucket.list_blobs(prefix=entity_name):
        if blob.name.endswith(".pdf"):
            blobs_found = True
            # Download the blob to a string
            pdf_bytes = blob.download_as_bytes()

            # Convert the bytes to a file-like object
            pdf_file = io.BytesIO(pdf_bytes)

            # Read the PDF file
            text = read_pdf(pdf_file)
            extracted_texts[blob.name] = text

    if not blobs_found:
        raise ValueError(f"No file found with prefix '{entity_name}' in bucket '{bucket_name}'. Please upload a PDF file for entity & try again")

    return extracted_texts


def read_pdfs_in_directory(directory_path):
    """
    Function to read all PDF files in a specified directory and extract their text.
    """
    extracted_texts = {}
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory_path, filename)
            text = read_pdf(file_path)
            extracted_texts[filename] = text
    return extracted_texts