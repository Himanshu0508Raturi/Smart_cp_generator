from app import db
from datetime import datetime
from sqlalchemy import Text

class Contract(db.Model):
    """Model for storing contract processing records"""
    id = db.Column(db.Integer, primary_key=True)
    contract_name = db.Column(db.String(255), nullable=False)
    fixture_recap_content = db.Column(Text)
    base_cp_content = db.Column(Text)
    negotiated_clauses_content = db.Column(Text)
    final_contract_content = db.Column(Text)
    extracted_clauses = db.Column(Text)  # JSON string of extracted clauses
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.String(50), default='draft')  # draft, processing, completed, error
    docx_path = db.Column(db.String(255))
    pdf_path = db.Column(db.String(255))
    
    def __repr__(self):
        return f'<Contract {self.contract_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'contract_name': self.contract_name,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'has_docx': bool(self.docx_path),
            'has_pdf': bool(self.pdf_path)
        }

class ProcessingLog(db.Model):
    """Model for storing processing logs and errors"""
    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer, db.ForeignKey('contract.id'), nullable=False)
    log_level = db.Column(db.String(20), nullable=False)  # INFO, WARNING, ERROR
    message = db.Column(Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    contract = db.relationship('Contract', backref=db.backref('logs', lazy=True))
    
    def __repr__(self):
        return f'<ProcessingLog {self.log_level}: {self.message[:50]}>'
