import re
import PyPDF2
from PyPDF2.generic import NameObject, TextStringObject
# Function to read PDF and extract text
def read_pdf(input_pdf_path):
    text = ""
    with open(input_pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text() or ""  # Extract text from each page
            text += page_text + "\n\n"  # Keep the paragraph structure intact
    return text.strip()
# Function to clean and normalize extracted text
def clean_tag(tag_content):
    tag_content = re.sub(r"[^a-zA-Z0-9\s]", "", tag_content)  # Remove special characters
    tag_content = re.sub(r'\s+', ' ', tag_content)  # Replace multiple spaces with a single space
    return tag_content.strip()
# Function to extract the paragraph below each specific tag
def extract_info_after_tags(text, predefined_tags):
    tag_data = {}
    for tag in predefined_tags:
        # Define the next tag or stop extraction after a paragraph or new heading
        next_tags = '|'.join(map(re.escape, predefined_tags))
        # Build the regex pattern to capture only the paragraph below the tag
        pattern = re.compile(
            rf"(?i){re.escape(tag)}\s*(.*?)(?=\n\s*\n|\s*(?:{next_tags})|\Z)",  # Stops at paragraph break or next tag
            re.DOTALL
        )
        match = pattern.search(text)
        if match:
            tag_content = match.group(1).strip()
            tag_data[tag] = clean_tag(tag_content)
            print(f"Extracted text for '{tag}': {tag_content[:100]}...")  # Print first 100 characters for debugging
        else:
            print(f"Tag '{tag}' not found in the document.")
    return tag_data
# Function to add/update metadata to a PDF
def add_metadata_to_pdf(input_pdf_path, output_pdf_path, tag_data):
    with open(input_pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()
        # Copy pages to the writer
        for page in reader.pages:
            writer.add_page(page)
        # Extract existing metadata
        existing_metadata = reader.metadata or {}
        # Add extracted tag data to the metadata
        for tag, content in tag_data.items():
            existing_metadata[NameObject(f"/{tag}")] = TextStringObject(content)
        # Add updated metadata to the writer
        writer.add_metadata(existing_metadata)
        # Write to a new PDF file
        with open(output_pdf_path, 'wb') as output_file:
            writer.write(output_file)
        print(f"Metadata added to {output_pdf_path}")
# Example usage:
input_pdf = "Z:/13_Case Studies/02_CCHMC/12U – iTransition (Children's Hospital)/12SU - iTransition Case Study.pdf"  # PDF from uploaded file
output_pdf = "Z:/13_Case Studies/02_CCHMC/12U – iTransition (Children's Hospital)/12SU - iTransition Case Study_with_metadata.pdf"  # Output PDF path
# Predefined tags to look for in the document
predefined_tags = ["The Challenge", "The Approach", "The Results"]
# Read the PDF and extract text
text = read_pdf(input_pdf)
# Extract relevant information based on predefined tags
tag_data = extract_info_after_tags(text, predefined_tags)
# Add extracted tag data to PDF metadata
add_metadata_to_pdf(input_pdf, output_pdf, tag_data)
# Function to view PDF metadata
def view_pdf_metadata(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        metadata = reader.metadata  # Get the PDF metadata
        # Print the metadata
        if metadata:
            print(f"Metadata for {file_path}:")
            for key, value in metadata.items():
                print(f"{key}: {value}")
        else:
            print(f"No metadata found for {file_path}.")
# View the metadata of the output PDF
view_pdf_metadata(output_pdf)

























