# Smart CP Generator - Contract Automation

A Flask-based web application that automates Charter Party contract generation by merging fixture recaps, base contracts, and negotiated clauses into final legal documents with AI-powered clause extraction.

## Features

- **Document Upload & Processing**: Support for TXT, DOC, DOCX, and PDF files
- **AI-Powered Clause Extraction**: Uses spaCy NLP for intelligent clause identification
- **Multiple Output Formats**: Generate contracts in Word (.docx) and PDF formats
- **In-Browser Preview**: View generated contracts before downloading
- **Contract Management**: History, search, and filtering capabilities
- **Responsive Design**: Professional UI built with Bootstrap 5
- **Local Storage**: No external database dependencies (uses SQLite)

## Technology Stack

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: Database ORM with SQLite
- **python-docx**: Word document processing
- **reportlab**: PDF generation
- **spaCy**: Natural Language Processing
- **PyPDF2**: PDF text extraction

### Frontend
- **Bootstrap 5**: Responsive UI framework
- **Font Awesome**: Icons
- **Vanilla JavaScript**: Client-side interactions
- **Custom CSS**: Professional styling

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Install System Dependencies

```bash
# For spaCy English model
python -m pip install spacy
python -m spacy download en_core_web_sm
