// Smart CP Generator - Main JavaScript

/**
 * Initialize the application
 */
document.addEventListener('DOMContentLoaded', function() {
    initializeTooltips();
    initializeFormValidation();
    initializeFileHandlers();
    initializeSearchFilters();
    
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('fade-in-up');
        }, index * 100);
    });
});

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize form validation
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * Initialize file upload handlers
 */
function initializeFileHandlers() {
    // File input change handlers
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            handleFileSelection(e.target);
        });
        
        // Add drag and drop functionality
        input.addEventListener('dragover', function(e) {
            e.preventDefault();
            e.target.classList.add('drag-over');
        });
        
        input.addEventListener('dragleave', function(e) {
            e.target.classList.remove('drag-over');
        });
        
        input.addEventListener('drop', function(e) {
            e.preventDefault();
            e.target.classList.remove('drag-over');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                e.target.files = files;
                handleFileSelection(e.target);
            }
        });
    });
}

/**
 * Handle file selection and validation
 */
function handleFileSelection(input) {
    const file = input.files[0];
    if (!file) return;
    
    // File size validation (16MB max)
    const maxSize = 16 * 1024 * 1024;
    if (file.size > maxSize) {
        showAlert('File size too large. Maximum size is 16MB.', 'error');
        input.value = '';
        return;
    }
    
    // File type validation
    const allowedTypes = ['text/plain', 'application/pdf', 
                         'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                         'application/msword'];
    const allowedExtensions = ['txt', 'pdf', 'docx', 'doc'];
    
    const fileExtension = file.name.split('.').pop().toLowerCase();
    
    if (!allowedTypes.includes(file.type) && !allowedExtensions.includes(fileExtension)) {
        showAlert('Invalid file type. Please select TXT, DOC, DOCX, or PDF files.', 'error');
        input.value = '';
        return;
    }
    
    // Clear corresponding text input
    const inputName = input.name.replace('_file', '_text');
    const textInput = document.querySelector(`[name="${inputName}"]`);
    if (textInput) {
        textInput.value = '';
    }
    
    // Show success feedback
    showFileInfo(input, file);
}

/**
 * Show file information
 */
function showFileInfo(input, file) {
    const fileInfo = document.createElement('div');
    fileInfo.className = 'file-info mt-2 p-2 bg-light rounded';
    fileInfo.innerHTML = `
        <small class="text-success">
            <i class="fas fa-check-circle me-1"></i>
            Selected: ${file.name} (${formatFileSize(file.size)})
        </small>
    `;
    
    // Remove existing file info
    const existingInfo = input.parentNode.querySelector('.file-info');
    if (existingInfo) {
        existingInfo.remove();
    }
    
    input.parentNode.appendChild(fileInfo);
}

/**
 * Format file size for display
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * Initialize search and filter functionality
 */
function initializeSearchFilters() {
    const searchInput = document.getElementById('search');
    const statusSelect = document.getElementById('status');
    
    if (searchInput) {
        // Add search icon
        const searchWrapper = document.createElement('div');
        searchWrapper.className = 'position-relative';
        searchInput.parentNode.insertBefore(searchWrapper, searchInput);
        searchWrapper.appendChild(searchInput);
        
        const searchIcon = document.createElement('i');
        searchIcon.className = 'fas fa-search position-absolute';
        searchIcon.style.cssText = 'right: 10px; top: 50%; transform: translateY(-50%); color: #6b7280;';
        searchWrapper.appendChild(searchIcon);
        
        // Add debounced search
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                if (this.value.length >= 3 || this.value.length === 0) {
                    // Auto-submit could be added here if needed
                }
            }, 300);
        });
    }
    
    if (statusSelect) {
        statusSelect.addEventListener('change', function() {
            // The form submission is handled in the template
        });
    }
}

/**
 * Show alert messages
 */
function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.container.mt-3') || document.querySelector('main');
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
    alert.innerHTML = `
        <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : type === 'success' ? 'check-circle' : 'info-circle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.insertBefore(alert, alertContainer.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}

/**
 * Handle contract processing form submission
 */
function handleContractSubmission(form) {
    const submitBtn = form.querySelector('[type="submit"]');
    const originalText = submitBtn.innerHTML;
    
    // Validate that at least one document is provided
    const hasFile = Array.from(form.querySelectorAll('input[type="file"]'))
        .some(input => input.files.length > 0);
    
    const hasText = Array.from(form.querySelectorAll('textarea'))
        .some(textarea => textarea.value.trim().length > 0);
    
    if (!hasFile && !hasText) {
        showAlert('Please provide at least one document (file upload or text input).', 'error');
        return false;
    }
    
    // Show processing state
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
    
    // Show progress indicator
    showProcessingProgress();
    
    return true;
}

/**
 * Show processing progress
 */
function showProcessingProgress() {
    const progressHTML = `
        <div id="processingProgress" class="mt-3">
            <div class="card">
                <div class="card-body">
                    <div class="d-flex align-items-center">
                        <div class="spinner-border spinner-border-sm text-primary me-3" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                        <div class="flex-grow-1">
                            <h6 class="mb-1">Processing Your Contract</h6>
                            <small class="text-muted">Analyzing documents and extracting clauses...</small>
                        </div>
                    </div>
                    <div class="progress mt-2" style="height: 4px;">
                        <div class="progress-bar progress-bar-striped progress-bar-animated" 
                             role="progressbar" style="width: 100%"></div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    const form = document.getElementById('uploadForm');
    if (form) {
        form.insertAdjacentHTML('afterend', progressHTML);
    }
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(text, element) {
    navigator.clipboard.writeText(text).then(function() {
        // Show success feedback
        const originalText = element.innerHTML;
        element.innerHTML = '<i class="fas fa-check me-1"></i>Copied!';
        element.classList.add('btn-success');
        
        setTimeout(() => {
            element.innerHTML = originalText;
            element.classList.remove('btn-success');
        }, 2000);
    }).catch(function() {
        showAlert('Failed to copy to clipboard', 'error');
    });
}

/**
 * Download functionality
 */
function downloadFile(url, filename) {
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

/**
 * Print contract content
 */
function printContract(containerId) {
    const content = document.getElementById(containerId);
    if (!content) return;
    
    const printWindow = window.open('', '_blank');
    const printContent = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>Charter Party Contract</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body { margin: 20px; font-family: 'Times New Roman', serif; }
                .contract-preview { line-height: 1.8; }
                @media print { 
                    .no-print { display: none; }
                    body { margin: 0; }
                }
            </style>
        </head>
        <body>
            <div class="contract-preview">
                ${content.innerHTML}
            </div>
        </body>
        </html>
    `;
    
    printWindow.document.write(printContent);
    printWindow.document.close();
    printWindow.focus();
    
    setTimeout(() => {
        printWindow.print();
        printWindow.close();
    }, 250);
}

/**
 * Handle fullscreen toggle
 */
function toggleFullscreen(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    if (!document.fullscreenElement) {
        element.requestFullscreen().catch(err => {
            console.log(`Error attempting to enable fullscreen: ${err.message}`);
        });
    } else {
        document.exitFullscreen();
    }
}

/**
 * Auto-save functionality for text inputs
 */
function initializeAutoSave() {
    const textAreas = document.querySelectorAll('textarea');
    
    textAreas.forEach(textarea => {
        const saveKey = `cp_generator_${textarea.name}`;
        
        // Load saved content
        const savedContent = localStorage.getItem(saveKey);
        if (savedContent && !textarea.value.trim()) {
            textarea.value = savedContent;
        }
        
        // Save on input
        textarea.addEventListener('input', function() {
            localStorage.setItem(saveKey, this.value);
        });
        
        // Clear on form submit
        const form = textarea.closest('form');
        if (form) {
            form.addEventListener('submit', function() {
                localStorage.removeItem(saveKey);
            });
        }
    });
}

/**
 * Initialize character count for textareas
 */
function initializeCharacterCount() {
    const textAreas = document.querySelectorAll('textarea');
    
    textAreas.forEach(textarea => {
        const counter = document.createElement('small');
        counter.className = 'text-muted character-count';
        counter.style.cssText = 'float: right; margin-top: 5px;';
        
        const updateCounter = () => {
            const count = textarea.value.length;
            counter.textContent = `${count} characters`;
        };
        
        textarea.addEventListener('input', updateCounter);
        textarea.parentNode.appendChild(counter);
        updateCounter();
    });
}

/**
 * Handle responsive tables
 */
function handleResponsiveTables() {
    const tables = document.querySelectorAll('.table');
    
    tables.forEach(table => {
        if (window.innerWidth < 768) {
            table.classList.add('table-sm');
        } else {
            table.classList.remove('table-sm');
        }
    });
}

// Initialize responsive handlers
window.addEventListener('resize', handleResponsiveTables);

/**
 * Keyboard shortcuts
 */
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + S to save (prevent default and show message)
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        showAlert('Auto-save is enabled. Your progress is automatically saved.', 'info');
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        const openModal = document.querySelector('.modal.show');
        if (openModal) {
            const modal = bootstrap.Modal.getInstance(openModal);
            if (modal) modal.hide();
        }
    }
});

// Initialize additional features when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeAutoSave();
    initializeCharacterCount();
    handleResponsiveTables();
});

// Export functions for global use
window.CPGenerator = {
    showAlert,
    copyToClipboard,
    downloadFile,
    printContract,
    toggleFullscreen,
    handleContractSubmission
};
