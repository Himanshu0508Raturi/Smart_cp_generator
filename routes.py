import os
import json
from flask import render_template, request, redirect, url_for, flash, send_file, jsonify
from werkzeug.utils import secure_filename
from app import app
from models import Contract
from document_processor import DocumentProcessor
from nlp_processor import NLPProcessor

# Initialize processors
doc_processor = DocumentProcessor()
nlp_processor = NLPProcessor()

ALLOWED_EXTENSIONS = {'txt', 'doc', 'docx', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main dashboard showing recent contracts and system overview"""
    all_contracts = Contract.get_all()
    recent_contracts = all_contracts[:5]  # Get first 5 (already sorted by date)
    total_contracts = len(all_contracts)
    completed_contracts = Contract.count_by_status('completed')
    
    stats = {
        'total': total_contracts,
        'completed': completed_contracts,
        'success_rate': round((completed_contracts / total_contracts * 100) if total_contracts > 0 else 0, 1)
    }
    
    return render_template('index.html', recent_contracts=recent_contracts, stats=stats)

@app.route('/upload', methods=['GET', 'POST'])
def upload_documents():
    """Handle document upload and processing"""
    if request.method == 'POST':
        contract_name = request.form.get('contract_name', '').strip()
        if not contract_name:
            flash('Contract name is required', 'error')
            return redirect(request.url)
        
        # Create new contract record
        contract = Contract(contract_name=contract_name, status='processing')
        contract.save()
        
        try:
            # Process each document type
            document_contents = {}
            
            # Handle fixture recap
            if 'fixture_recap_file' in request.files and request.files['fixture_recap_file'].filename:
                file = request.files['fixture_recap_file']
                if allowed_file(file.filename):
                    content = doc_processor.extract_text_from_file(file)
                    document_contents['fixture_recap'] = content
                    contract.fixture_recap_content = content
            elif request.form.get('fixture_recap_text'):
                content = request.form.get('fixture_recap_text').strip()
                document_contents['fixture_recap'] = content
                contract.fixture_recap_content = content
            
            # Handle base CP
            if 'base_cp_file' in request.files and request.files['base_cp_file'].filename:
                file = request.files['base_cp_file']
                if allowed_file(file.filename):
                    content = doc_processor.extract_text_from_file(file)
                    document_contents['base_cp'] = content
                    contract.base_cp_content = content
            elif request.form.get('base_cp_text'):
                content = request.form.get('base_cp_text').strip()
                document_contents['base_cp'] = content
                contract.base_cp_content = content
            
            # Handle negotiated clauses
            if 'negotiated_clauses_file' in request.files and request.files['negotiated_clauses_file'].filename:
                file = request.files['negotiated_clauses_file']
                if allowed_file(file.filename):
                    content = doc_processor.extract_text_from_file(file)
                    document_contents['negotiated_clauses'] = content
                    contract.negotiated_clauses_content = content
            elif request.form.get('negotiated_clauses_text'):
                content = request.form.get('negotiated_clauses_text').strip()
                document_contents['negotiated_clauses'] = content
                contract.negotiated_clauses_content = content
            
            # Validate that we have at least one document
            if not any(document_contents.values()):
                raise ValueError("At least one document must be provided")
            
            # Process with NLP
            extracted_clauses = nlp_processor.extract_clauses(document_contents)
            contract.extracted_clauses = json.dumps(extracted_clauses)
            
            # Generate final contract
            final_contract = doc_processor.merge_documents(document_contents, extracted_clauses)
            contract.final_contract_content = final_contract
            
            # Generate output files
            docx_path, pdf_path = doc_processor.generate_output_files(
                final_contract, contract.id, contract_name
            )
            contract.docx_path = docx_path
            contract.pdf_path = pdf_path
            contract.status = 'completed'
            
            # Save contract
            contract.save()
            flash('Contract processed successfully!', 'success')
            return redirect(url_for('preview_contract', contract_id=contract.id))
            
        except Exception as e:
            contract.status = 'error'
            contract.save()
            flash(f'Error processing contract: {str(e)}', 'error')
            app.logger.error(f'Contract processing error: {str(e)}')
    
    return render_template('upload.html')

@app.route('/preview/<contract_id>')
def preview_contract(contract_id):
    """Preview generated contract"""
    contract = Contract.load(contract_id)
    if not contract:
        flash('Contract not found', 'error')
        return redirect(url_for('index'))
    return render_template('preview.html', contract=contract)

@app.route('/history')
def contract_history():
    """View all contracts with filtering and search"""
    status_filter = request.args.get('status', '')
    search_term = request.args.get('search', '')
    
    all_contracts = Contract.get_all()
    
    # Apply filters
    if status_filter:
        all_contracts = [c for c in all_contracts if c.status == status_filter]
    
    if search_term:
        all_contracts = [c for c in all_contracts if search_term.lower() in c.contract_name.lower()]
    
    # Simple pagination simulation (for template compatibility)
    class MockPagination:
        def __init__(self, items):
            self.items = items
            self.has_prev = False
            self.has_next = False
            self.prev_num = None
            self.next_num = None
    
    contracts = MockPagination(all_contracts)
    
    return render_template('history.html', contracts=contracts, 
                         status_filter=status_filter, search_term=search_term)

@app.route('/download/<contract_id>/<file_type>')
def download_file(contract_id, file_type):
    """Download generated contract files"""
    contract = Contract.load(contract_id)
    if not contract:
        flash('Contract not found', 'error')
        return redirect(url_for('index'))
    
    if file_type == 'docx' and contract.docx_path:
        return send_file(contract.docx_path, as_attachment=True, 
                        download_name=f"{contract.contract_name}.docx")
    elif file_type == 'pdf' and contract.pdf_path:
        return send_file(contract.pdf_path, as_attachment=True,
                        download_name=f"{contract.contract_name}.pdf")
    else:
        flash('File not found', 'error')
        return redirect(url_for('preview_contract', contract_id=contract_id))

@app.route('/delete/<contract_id>', methods=['POST'])
def delete_contract(contract_id):
    """Delete a contract and its associated files"""
    contract = Contract.load(contract_id)
    if not contract:
        flash('Contract not found', 'error')
        return redirect(url_for('contract_history'))
    
    try:
        # Delete associated files
        if contract.docx_path and os.path.exists(contract.docx_path):
            os.remove(contract.docx_path)
        if contract.pdf_path and os.path.exists(contract.pdf_path):
            os.remove(contract.pdf_path)
        
        # Delete contract file
        contract_file = os.path.join(app.config['CONTRACTS_STORAGE'], f'{contract.id}.json')
        if os.path.exists(contract_file):
            os.remove(contract_file)
        
        flash('Contract deleted successfully', 'success')
    except Exception as e:
        flash(f'Error deleting contract: {str(e)}', 'error')
        app.logger.error(f'Contract deletion error: {str(e)}')
    
    return redirect(url_for('contract_history'))

@app.errorhandler(404)
def not_found(error):
    return render_template('base.html', error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('base.html', error_message="Internal server error"), 500
