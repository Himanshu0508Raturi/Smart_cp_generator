import os
import json
import logging
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure session storage
app.config['CONTRACTS_STORAGE'] = 'contracts_data'

# Configure upload settings
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['GENERATED_FOLDER'] = 'generated'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload and generated directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['GENERATED_FOLDER'], exist_ok=True)

# Ensure contracts storage directory exists
os.makedirs(app.config['CONTRACTS_STORAGE'], exist_ok=True)

# Add custom template filter for JSON parsing
@app.template_filter('fromjson')
def fromjson_filter(value):
    if value:
        try:
            return json.loads(value)
        except (ValueError, TypeError):
            return {}
    return {}

# Import models and routes
import models
import routes

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
