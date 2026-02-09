# Image Captioning Application

A state-of-the-art web application that generates accurate, descriptive captions for images using deep learning models.

## 🌟 Features

- **AI-Powered Captioning**: Uses BLIP (Bootstrapping Language-Image Pre-training) model for accurate image descriptions
- **Dual Caption Modes**: 
  - Standard captions for quick descriptions
  - Detailed captions for more comprehensive descriptions
- **Modern UI**: Premium dark theme with glassmorphism effects and smooth animations
- **Drag & Drop**: Easy image upload with drag-and-drop support
- **Multiple Formats**: Supports PNG, JPG, GIF, BMP, and WebP images
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Real-time Processing**: Fast caption generation with loading indicators

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 4-8GB RAM (for model inference)

### Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd ImageCaptioning
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   > **Note**: First-time installation will download the BLIP model (~2-3GB). This may take several minutes depending on your internet connection.

### Running the Application

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

3. **Upload an image** and click "Generate Caption" to see the AI in action!

## 📖 Usage

### Basic Caption Generation

1. Click the upload area or drag and drop an image
2. Click "Generate Caption" button
3. Wait for the AI to process (usually 2-5 seconds)
4. View your generated caption!

### Detailed Caption Generation

1. Upload an image
2. Click "Detailed Caption" button
3. Get a more comprehensive description of your image

### Keyboard Shortcuts

- `Ctrl/Cmd + V`: Paste image from clipboard
- `Esc`: Reset and upload new image

## 🏗️ Project Structure

```
ImageCaptioning/
├── app.py                  # Flask backend server
├── model_loader.py         # BLIP model loading and inference
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html         # Main HTML page
├── static/
│   ├── css/
│   │   └── style.css      # Styling and animations
│   └── js/
│       └── main.js        # Frontend logic
└── README.md              # This file
```

## 🔧 API Documentation

### POST /upload

Upload an image and generate a caption.

**Request**:
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body:
  - `image`: Image file (required)
  - `type`: Caption type - "default" or "detailed" (optional, default: "default")

**Response**:
```json
{
  "success": true,
  "caption": "a dog sitting on a beach",
  "filename": "image.jpg"
}
```

**Error Response**:
```json
{
  "error": "Error message"
}
```

### GET /health

Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "service": "Image Captioning API"
}
```

## 🧠 Model Information

This application uses the **BLIP (Bootstrapping Language-Image Pre-training)** model:

- **Model**: `Salesforce/blip-image-captioning-large`
- **Architecture**: Vision-Language Transformer
- **Performance**: State-of-the-art accuracy on image captioning benchmarks
- **Inference**: Supports both CPU and GPU (automatically detected)

## ⚙️ Configuration

### GPU Support

The application automatically detects and uses GPU if available. To use CPU only:

```python
# In model_loader.py, modify get_device():
def get_device():
    return "cpu"
```

### Model Selection

To use a different model, modify `model_loader.py`:

```python
# Change the model_name variable
model_name = "Salesforce/blip-image-captioning-base"  # Lighter version
# or
model_name = "Salesforce/blip2-opt-2.7b"  # BLIP-2 (more advanced)
```

## 🐛 Troubleshooting

### Model Download Issues

If the model fails to download:
1. Check your internet connection
2. Ensure you have enough disk space (~3GB)
3. Try downloading manually from HuggingFace

### Memory Issues

If you encounter out-of-memory errors:
1. Use the base model instead of large
2. Close other applications
3. Reduce image size before uploading

### Port Already in Use

If port 5000 is already in use:
```python
# In app.py, change the port:
app.run(debug=True, host='0.0.0.0', port=8000)
```

## 📝 License

This project is open source and available for educational and commercial use.

## 🙏 Acknowledgments

- **BLIP Model**: Salesforce Research
- **HuggingFace**: For the Transformers library
- **Flask**: For the web framework

## 🔮 Future Enhancements

- [ ] Batch image processing
- [ ] Multiple language support
- [ ] Image editing suggestions
- [ ] Caption history and favorites
- [ ] API key authentication
- [ ] Docker containerization

## 📧 Support

For issues, questions, or suggestions, please create an issue in the project repository.

---

**Made with ❤️ using Deep Learning**
