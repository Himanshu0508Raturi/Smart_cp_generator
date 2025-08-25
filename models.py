import os
import json
import uuid
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Contract:
    """Data class for storing contract processing records"""
    contract_name: str
    fixture_recap_content: Optional[str] = None
    base_cp_content: Optional[str] = None
    negotiated_clauses_content: Optional[str] = None
    final_contract_content: Optional[str] = None
    extracted_clauses: Optional[str] = None  # JSON string of extracted clauses
    status: str = 'draft'  # draft, processing, completed, error
    docx_path: Optional[str] = None
    pdf_path: Optional[str] = None
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
    
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
    
    def save(self):
        """Save contract to file storage"""
        from app import app
        self.updated_at = datetime.utcnow()
        storage_path = os.path.join(app.config['CONTRACTS_STORAGE'], f'{self.id}.json')
        contract_data = asdict(self)
        # Convert datetime objects to strings for JSON serialization
        contract_data['created_at'] = self.created_at.isoformat() if self.created_at else None
        contract_data['updated_at'] = self.updated_at.isoformat() if self.updated_at else None
        
        with open(storage_path, 'w') as f:
            json.dump(contract_data, f, indent=2)
    
    @classmethod
    def load(cls, contract_id: str):
        """Load contract from file storage"""
        from app import app
        storage_path = os.path.join(app.config['CONTRACTS_STORAGE'], f'{contract_id}.json')
        if not os.path.exists(storage_path):
            return None
        
        with open(storage_path, 'r') as f:
            contract_data = json.load(f)
        
        # Convert string dates back to datetime objects
        if contract_data['created_at']:
            contract_data['created_at'] = datetime.fromisoformat(contract_data['created_at'])
        if contract_data['updated_at']:
            contract_data['updated_at'] = datetime.fromisoformat(contract_data['updated_at'])
        
        return cls(**contract_data)
    
    @classmethod
    def get_all(cls):
        """Get all contracts from file storage"""
        from app import app
        contracts = []
        storage_dir = app.config['CONTRACTS_STORAGE']
        
        if os.path.exists(storage_dir):
            for filename in os.listdir(storage_dir):
                if filename.endswith('.json'):
                    contract_id = filename[:-5]  # Remove .json extension
                    contract = cls.load(contract_id)
                    if contract:
                        contracts.append(contract)
        
        # Sort by updated_at descending
        contracts.sort(key=lambda x: x.updated_at if x.updated_at else datetime.min, reverse=True)
        return contracts
    
    @classmethod
    def count_by_status(cls, status=None):
        """Count contracts by status"""
        contracts = cls.get_all()
        if status:
            return len([c for c in contracts if c.status == status])
        return len(contracts)

