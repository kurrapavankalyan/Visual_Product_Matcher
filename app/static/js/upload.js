// Upload functionality

const fileInput = document.getElementById('file-input');
const previewContainer = document.getElementById('preview-container');
const previewImage = document.getElementById('preview-image');
const uploadForm = document.getElementById('upload-form');
const urlForm = document.getElementById('url-form');

// File input change handler
if (fileInput) {
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            displayPreview(file);
        }
    });
}

// Drag and drop functionality
const fileLabel = document.querySelector('.file-label');
if (fileLabel) {
    fileLabel.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileLabel.style.borderColor = 'var(--primary-color)';
    });
    
    fileLabel.addEventListener('dragleave', (e) => {
        e.preventDefault();
        fileLabel.style.borderColor = 'var(--border-color)';
    });
    
    fileLabel.addEventListener('drop', (e) => {
        e.preventDefault();
        fileLabel.style.borderColor = 'var(--border-color)';
        
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            fileInput.files = e.dataTransfer.files;
            displayPreview(file);
        }
    });
}

// Display image preview
function displayPreview(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        previewContainer.style.display = 'block';
    };
    reader.readAsDataURL(file);
}

// Remove image
function removeImage() {
    fileInput.value = '';
    previewContainer.style.display = 'none';
    previewImage.src = '';
}

// Handle file upload form submission
if (uploadForm) {
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(uploadForm);
        
        if (!fileInput.files[0]) {
            showError('Please select an image');
            return;
        }
        
        showLoading();
        
        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.success) {
                displayResults(data);
            } else {
                showError(data.error || 'An error occurred');
            }
        } catch (error) {
            showError('Network error: ' + error.message);
        } finally {
            hideLoading();
        }
    });
}

// Handle URL form submission
if (urlForm) {
    urlForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(urlForm);
        const imageUrl = formData.get('image_url');
        
        if (!imageUrl) {
            showError('Please enter an image URL');
            return;
        }
        
        showLoading();
        
        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.success) {
                displayResults(data);
            } else {
                showError(data.error || 'An error occurred');
            }
        } catch (error) {
            showError('Network error: ' + error.message);
        } finally {
            hideLoading();
        }
    });
}