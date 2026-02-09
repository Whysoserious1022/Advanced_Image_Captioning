"""
Model Loader for Image Captioning
Handles loading and caching of the BLIP-2 model
"""

import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for model caching
_model = None
_processor = None
_device = None


def get_device():
    """Detect and return the best available device (GPU/CPU)"""
    global _device
    if _device is None:
        if torch.cuda.is_available():
            _device = "cuda"
            logger.info("Using GPU (CUDA) for inference")
        else:
            _device = "cpu"
            logger.info("Using CPU for inference")
    return _device


def get_model():
    """
    Load and return the BLIP model and processor.
    Uses singleton pattern to avoid reloading.
    
    Returns:
        tuple: (model, processor)
    """
    global _model, _processor
    
    if _model is None or _processor is None:
        logger.info("Loading BLIP model... This may take a few minutes on first run.")
        
        try:
            # Using BLIP (lighter version) - can be upgraded to BLIP-2 if needed
            model_name = "Salesforce/blip-image-captioning-large"
            
            # Load processor and model
            _processor = BlipProcessor.from_pretrained(model_name)
            _model = BlipForConditionalGeneration.from_pretrained(model_name)
            
            # Move model to appropriate device
            device = get_device()
            _model = _model.to(device)
            
            # Enable half precision for faster inference on GPU
            if device == "cuda":
                _model = _model.half()
                logger.info("Enabled half-precision (fp16) for faster GPU inference")
            
            # Set to evaluation mode
            _model.eval()
            
            logger.info(f"Model loaded successfully on {device}")
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    return _model, _processor


def generate_caption(image, max_length=50, num_beams=4):
    """
    Generate a caption for the given image.
    
    Args:
        image: PIL Image object
        max_length: Maximum length of generated caption
        num_beams: Number of beams for beam search
        
    Returns:
        str: Generated caption
    """
    try:
        model, processor = get_model()
        device = get_device()
        
        # Preprocess image
        inputs = processor(image, return_tensors="pt").to(device)
        
        # Generate caption
        with torch.no_grad():
            output = model.generate(
                **inputs,
                max_length=max_length,
                num_beams=num_beams,
                early_stopping=True
            )
        
        # Decode and return caption
        caption = processor.decode(output[0], skip_special_tokens=True)
        logger.info(f"Generated caption: {caption}")
        
        return caption
        
    except Exception as e:
        logger.error(f"Error generating caption: {str(e)}")
        raise


def generate_detailed_caption(image):
    """
    Generate a more detailed caption using conditional generation.
    Optimized for faster inference with enhanced quality.
    
    Args:
        image: PIL Image object
        
    Returns:
        str: Generated detailed caption
    """
    try:
        model, processor = get_model()
        device = get_device()
        
        # Use an enhanced prompt for more vivid, detailed captions
        text_prompt = "a detailed description of"
        
        inputs = processor(image, text_prompt, return_tensors="pt").to(device)
        
        # Use half precision for faster inference on GPU
        if device == "cuda":
            inputs = {k: v.half() if v.dtype == torch.float32 else v for k, v in inputs.items()}
        
        with torch.no_grad():
            output = model.generate(
                **inputs,
                max_length=70,  # Increased for more detailed captions
                num_beams=4,    # Balanced for quality and speed
                early_stopping=True,
                do_sample=False,  # Deterministic for consistency
                repetition_penalty=1.2  # Avoid repetitive words
            )
        
        caption = processor.decode(output[0], skip_special_tokens=True)
        
        # Clean up the caption if it starts with the prompt
        if caption.lower().startswith("a detailed description of"):
            caption = caption[len("a detailed description of"):].strip()
        
        logger.info(f"Generated detailed caption: {caption}")
        
        return caption
        
    except Exception as e:
        logger.error(f"Error generating detailed caption: {str(e)}")
        raise
