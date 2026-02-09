// Image Captioning Frontend Logic

let selectedImage = null;
let selectedFile = null;

// DOM Elements
const uploadZone = document.getElementById('uploadZone');
const fileInput = document.getElementById('fileInput');
const previewContainer = document.getElementById('previewContainer');
const imagePreview = document.getElementById('imagePreview');
const generateDetailedBtn = document.getElementById('generateDetailedBtn');
const newImageBtn = document.getElementById('newImageBtn');
const captionContainer = document.getElementById('captionContainer');
const captionText = document.getElementById('captionText');
const loading = document.getElementById('loading');
const errorMessage = document.getElementById('errorMessage');

// Upload Zone Click Handler
uploadZone.addEventListener('click', () => {
    fileInput.click();
});

// File Input Change Handler
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        handleFileSelect(file);
    }
});

// Drag and Drop Handlers
uploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadZone.classList.add('dragover');
});

uploadZone.addEventListener('dragleave', () => {
    uploadZone.classList.remove('dragover');
});

uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.classList.remove('dragover');

    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        handleFileSelect(file);
    } else {
        showError('Please drop a valid image file');
    }
});

// Handle File Selection
function handleFileSelect(file) {
    // Validate file type
    const validTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/bmp', 'image/webp'];
    if (!validTypes.includes(file.type)) {
        showError('Invalid file type. Please upload a PNG, JPG, GIF, BMP, or WebP image.');
        return;
    }

    // Validate file size (16MB max)
    if (file.size > 16 * 1024 * 1024) {
        showError('File too large. Maximum size is 16MB.');
        return;
    }

    selectedFile = file;

    // Create preview
    const reader = new FileReader();
    reader.onload = (e) => {
        selectedImage = e.target.result;
        imagePreview.src = selectedImage;
        previewContainer.classList.add('active');
        captionContainer.classList.remove('active');
        hideError();
    };
    reader.readAsDataURL(file);
}

// Generate Caption (Detailed only)
generateDetailedBtn.addEventListener('click', () => {
    generateCaption('detailed');
});

// Generate Caption Function
async function generateCaption(type = 'default') {
    if (!selectedFile) {
        showError('Please select an image first');
        return;
    }

    // Show loading state
    loading.classList.add('active');
    captionContainer.classList.remove('active');
    hideError();

    // Prepare form data
    const formData = new FormData();
    formData.append('image', selectedFile);
    formData.append('type', type);

    try {
        // Send request to backend
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        // Hide loading
        loading.classList.remove('active');

        if (response.ok && data.success) {
            // Display caption
            captionText.textContent = data.caption;
            captionContainer.classList.add('active');
        } else {
            // Show error
            showError(data.error || 'Failed to generate caption. Please try again.');
        }

    } catch (error) {
        loading.classList.remove('active');
        showError('Network error. Please check your connection and try again.');
        console.error('Error:', error);
    }
}

// New Image Button Handler
newImageBtn.addEventListener('click', () => {
    resetApp();
});

// Reset Application
function resetApp() {
    selectedImage = null;
    selectedFile = null;
    fileInput.value = '';
    previewContainer.classList.remove('active');
    captionContainer.classList.remove('active');
    loading.classList.remove('active');
    hideError();
}

// Show Error Message
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.add('active');

    // Auto-hide after 5 seconds
    setTimeout(() => {
        hideError();
    }, 5000);
}

// Hide Error Message
function hideError() {
    errorMessage.classList.remove('active');
}

// Keyboard Shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + V to paste image
    if ((e.ctrlKey || e.metaKey) && e.key === 'v') {
        navigator.clipboard.read().then(items => {
            for (let item of items) {
                for (let type of item.types) {
                    if (type.startsWith('image/')) {
                        item.getType(type).then(blob => {
                            const file = new File([blob], 'pasted-image.png', { type });
                            handleFileSelect(file);
                        });
                        break;
                    }
                }
            }
        }).catch(err => {
            console.log('Clipboard access denied or no image found');
        });
    }

    // Escape to reset
    if (e.key === 'Escape') {
        resetApp();
    }
});

// Prevent default drag behavior on document
document.addEventListener('dragover', (e) => {
    e.preventDefault();
});

document.addEventListener('drop', (e) => {
    e.preventDefault();
});

// Console welcome message
console.log('%c🎨 Image Captioning App', 'color: #667eea; font-size: 20px; font-weight: bold;');
console.log('%cPowered by BLIP Deep Learning Model', 'color: #764ba2; font-size: 14px;');
