"""
PDF Processor Module
Handles PDF and DOCX file processing for CV extraction
"""

import PyPDF2
import docx
import streamlit as st
from io import BytesIO


class PDFProcessor:
    """Handle PDF and DOCX file processing"""
    
    def __init__(self):
        pass
    
    def extract_text(self, uploaded_file) -> str:
        """
        Extract text from uploaded PDF or DOCX file
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            str: Extracted text content
        """
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'pdf':
            return self._extract_from_pdf(uploaded_file)
        elif file_extension == 'docx':
            return self._extract_from_docx(uploaded_file)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def _extract_from_pdf(self, uploaded_file) -> str:
        """Extract text from PDF file"""
        try:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(BytesIO(uploaded_file.read()))
            
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            
            return text.strip()
            
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def _extract_from_docx(self, uploaded_file) -> str:
        """Extract text from DOCX file"""
        try:
            # Create a DOCX document object
            doc = docx.Document(BytesIO(uploaded_file.read()))
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text.strip()
            
        except Exception as e:
            raise Exception(f"Error extracting text from DOCX: {str(e)}")
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize extracted text
        
        Args:
            text: Raw extracted text
            
        Returns:
            str: Cleaned text
        """
        # Remove extra whitespace and normalize
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line and len(line) > 1:  # Skip empty lines and single characters
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def extract_sections(self, text: str) -> dict:
        """
        Extract different sections from CV text
        
        Args:
            text: CV text content
            
        Returns:
            dict: Dictionary with extracted sections
        """
        sections = {
            'personal_info': '',
            'summary': '',
            'experience': '',
            'education': '',
            'skills': '',
            'other': ''
        }
        
        # Common section headers
        section_keywords = {
            'summary': ['summary', 'profile', 'objective', 'about'],
            'experience': ['experience', 'employment', 'work history', 'professional experience'],
            'education': ['education', 'academic', 'qualifications'],
            'skills': ['skills', 'technical skills', 'competencies', 'expertise'],
        }
        
        lines = text.lower().split('\n')
        current_section = 'other'
        
        for line in lines:
            line_lower = line.strip().lower()
            
            # Check if this line indicates a new section
            for section, keywords in section_keywords.items():
                if any(keyword in line_lower for keyword in keywords):
                    current_section = section
                    break
            
            # Add content to current section
            if line.strip():
                sections[current_section] += line + '\n'
        
        # Clean up sections
        for key in sections:
            sections[key] = sections[key].strip()
        
        return sections
