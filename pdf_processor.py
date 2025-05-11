from pypdf import PdfReader
import os
import re
import streamlit as st
from io import BytesIO

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF
    """
    try:
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            num_pages = len(reader.pages)
            
            # Extract text from each page
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                page_text = page.extract_text()
                
                if page_text:
                    # Clean up text
                    page_text = clean_text(page_text)
                    text += f"\n--- Page {page_num+1} ---\n{page_text}\n"
        
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        return ""

def extract_text_from_pdf_bytes(pdf_bytes):
    """
    Extract text from PDF bytes.
    
    Args:
        pdf_bytes (bytes): PDF content as bytes
        
    Returns:
        str: Extracted text from the PDF
    """
    try:
        text = ""
        reader = PdfReader(BytesIO(pdf_bytes))
        num_pages = len(reader.pages)
        
        # Extract text from each page
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            page_text = page.extract_text()
            
            if page_text:
                # Clean up text
                page_text = clean_text(page_text)
                text += f"\n--- Page {page_num+1} ---\n{page_text}\n"
        
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF bytes: {str(e)}")
        return ""

def clean_text(text):
    """
    Clean extracted text by removing extra whitespace and normalizing line breaks.
    
    Args:
        text (str): Raw text extracted from PDF
        
    Returns:
        str: Cleaned text
    """
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove extra line breaks
    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    # Trim leading/trailing whitespace
    text = text.strip()
    
    return text

def extract_soil_data_from_text(text):
    """
    Extract structured soil data from the extracted text.
    This is a basic implementation and may need to be enhanced based on the actual PDF structure.
    
    Args:
        text (str): Extracted text from soil survey PDF
        
    Returns:
        dict: Structured soil data
    """
    soil_data = {
        "soil_types": [],
        "locations": [],
        "characteristics": {}
    }
    
    # Extract soil types (basic implementation)
    soil_type_patterns = [
        r'(?i)soil type[s]?:\s*([^\n]+)',
        r'(?i)([a-z\s]+) soil[s]?',
        r'(?i)soil classification[s]?:\s*([^\n]+)'
    ]
    
    for pattern in soil_type_patterns:
        matches = re.findall(pattern, text)
        if matches:
            soil_data["soil_types"].extend([match.strip() for match in matches])
    
    # Extract locations
    location_patterns = [
        r'(?i)location[s]?:\s*([^\n]+)',
        r'(?i)area[s]?:\s*([^\n]+)',
        r'(?i)region[s]?:\s*([^\n]+)'
    ]
    
    for pattern in location_patterns:
        matches = re.findall(pattern, text)
        if matches:
            soil_data["locations"].extend([match.strip() for match in matches])
    
    # Extract soil characteristics
    characteristic_patterns = {
        "pH": r'(?i)pH[\s:]+([0-9\.]+)[^\n]*',
        "texture": r'(?i)texture[\s:]+([^\n,;]+)',
        "drainage": r'(?i)drainage[\s:]+([^\n,;]+)',
        "fertility": r'(?i)fertility[\s:]+([^\n,;]+)'
    }
    
    for char_name, pattern in characteristic_patterns.items():
        matches = re.findall(pattern, text)
        if matches:
            soil_data["characteristics"][char_name] = [match.strip() for match in matches]
    
    return soil_data
