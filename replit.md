# Smart CP Generator - Contract Automation

## Overview

Smart CP Generator is a Flask-based web application that automates Charter Party contract generation by intelligently merging fixture recaps, base contracts, and negotiated clauses into final legal documents. The system uses AI-powered Natural Language Processing to extract and analyze contract clauses, providing a streamlined workflow for maritime contract creation with support for multiple document formats and professional output generation.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Framework
- **Flask Application**: Python web framework serving as the core application server with SQLAlchemy ORM for database operations
- **Modular Design**: Separation of concerns with dedicated modules for document processing (`document_processor.py`), NLP operations (`nlp_processor.py`), and data models (`models.py`)
- **File Storage**: Local file system storage for uploaded documents and generated contracts with configurable upload limits (16MB)

### Database Design
- **SQLite Database**: Local storage solution using SQLite for development and simple deployment
- **Contract Model**: Stores contract metadata, processing status, file paths, and content with timestamps
- **ProcessingLog Model**: Tracks processing logs and errors with relationship to contracts for debugging and audit trails

### Document Processing Pipeline
- **Multi-format Support**: Handles TXT, DOC, DOCX, and PDF file uploads with specialized extractors for each format
- **Text Extraction**: Uses python-docx for Word documents and PyPDF2 for PDF text extraction
- **Document Generation**: Creates output in both Word (.docx) using python-docx and PDF using reportlab

### Natural Language Processing
- **spaCy Integration**: English language model (en_core_web_sm) for clause identification and text analysis
- **Pattern Matching**: Custom patterns for common contract elements like payment terms, laytime clauses, and cargo specifications
- **Clause Classification**: Automatic extraction and categorization of contract clauses using linguistic patterns

### Frontend Architecture
- **Bootstrap 5**: Responsive UI framework for professional styling and mobile compatibility
- **Vanilla JavaScript**: Client-side interactions for form validation, file handling, and dynamic content updates
- **Template Engine**: Jinja2 templating with base template inheritance for consistent layout

### Application Flow
- **Upload Interface**: Multi-step form for uploading fixture recap, base CP, and negotiated clauses
- **Processing Pipeline**: Automatic text extraction, NLP analysis, and document merging
- **Preview System**: In-browser contract preview before download
- **History Management**: Contract tracking with search and filtering capabilities

## External Dependencies

### Core Python Libraries
- **Flask**: Web framework and request handling
- **SQLAlchemy**: Database ORM and query builder
- **python-docx**: Word document creation and manipulation
- **reportlab**: PDF generation and formatting
- **PyPDF2**: PDF text extraction capabilities

### Natural Language Processing
- **spaCy**: NLP library with English language model (en_core_web_sm)
- **spaCy Matcher**: Pattern matching for contract clause identification

### Frontend Dependencies
- **Bootstrap 5**: CSS framework loaded via CDN
- **Font Awesome**: Icon library for UI elements
- **No external JavaScript frameworks**: Pure vanilla JavaScript implementation

### Development Tools
- **Werkzeug**: WSGI utilities and development server
- **ProxyFix**: Middleware for handling proxy headers in deployment

### Storage Requirements
- **Local File System**: No external cloud storage dependencies
- **SQLite**: No external database server required
- **Upload Directory**: Temporary storage for uploaded files
- **Generated Directory**: Storage for output documents