import io
import aiohttp
from PIL import Image
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)

async def generate_image(prompt: str, width: int = 1024, height: int = 1024) -> bytes:
    """
    Generate an image using Pollinations.ai API
    
    Args:
        prompt: Text description of the image
        width: Image width (default: 1024)
        height: Image height (default: 1024)
    
    Returns:
        bytes: Image data
    """
    # Enhance prompt with artistic styling
    enhanced_prompt = f"{prompt}, high quality, detailed, 4k, beautiful, artistic"
    
    # Build the URL with parameters
    url = f"https://image.pollinations.ai/prompt/{enhanced_prompt}"
    params = {
        "width": width,
        "height": height,
        "nologo": "true",
        "seed": "random",
        "n": "1"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=30) as response:
                if response.status == 200:
                    image_data = await response.read()
                    # Validate it's a valid image
                    try:
                        Image.open(io.BytesIO(image_data))
                        return image_data
                    except Exception:
                        raise Exception("Generated content is not a valid image")
                else:
                    error_text = await response.text()
                    raise Exception(f"API returned status {response.status}: {error_text[:100]}")
    except aiohttp.ClientError as e:
        logger.error(f"Network error generating image: {e}")
        raise Exception(f"Network error: {str(e)}")
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        raise

async def shorten_url(url: str) -> str:
    """
    Shorten a URL using spoo.me API
    
    Args:
        url: URL to shorten
    
    Returns:
        str: Shortened URL
    """
    # Validate URL format
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://spoo.me/",
                data={'url': url},
                timeout=10
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('short_url', url)
                else:
                    error_text = await response.text()
                    raise Exception(f"API returned status {response.status}: {error_text[:100]}")
    except aiohttp.ClientError as e:
        logger.error(f"Network error shortening URL: {e}")
        raise Exception(f"Network error: {str(e)}")
    except Exception as e:
        logger.error(f"Error shortening URL: {e}")
        raise

async def convert_image(image_bytes: bytes, target_format: str) -> bytes:
    """
    Convert image to specified format
    
    Args:
        image_bytes: Original image data
        target_format: Target format (png, jpg, webp, etc.)
    
    Returns:
        bytes: Converted image data
    """
    try:
        # Open the image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Get original format
        original_format = image.format.lower() if image.format else 'unknown'
        
        # Handle special cases
        target_format_lower = target_format.lower()
        
        # Convert RGBA to RGB for JPEG
        if target_format_lower in ['jpg', 'jpeg']:
            if image.mode == 'RGBA':
                # Create white background
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[3])
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')
        elif image.mode == 'P':
            image = image.convert('RGB')
        
        # Save to bytes
        output = io.BytesIO()
        save_format = 'JPEG' if target_format_lower in ['jpg', 'jpeg'] else target_format_lower.upper()
        
        # Set quality for JPEG/WEBP
        if save_format in ['JPEG', 'WEBP']:
            image.save(output, format=save_format, quality=95, optimize=True)
        else:
            image.save(output, format=save_format, optimize=True)
        
        output.seek(0)
        return output.getvalue()
        
    except Exception as e:
        logger.error(f"Image conversion error: {e}")
        raise Exception(f"Failed to convert image: {str(e)}")

def is_valid_image_format(format_name: str) -> bool:
    """Check if the format is supported"""
    return format_name.lower() in SUPPORTED_FORMATS

def validate_url(url: str) -> Tuple[bool, str]:
    """
    Validate and format URL
    
    Returns:
        Tuple[bool, str]: (is_valid, formatted_url)
    """
    url = url.strip()
    if not url:
        return False, "URL cannot be empty"
    
    if not any(url.startswith(prefix) for prefix in ['http://', 'https://']):
        url = 'https://' + url
    
    # Basic URL validation
    if ' ' in url:
        return False, "URL cannot contain spaces"
    
    if not '.' in url or not any(tld in url for tld in ['.com', '.org', '.net', '.io', '.co', '.uk']):
        return False, "Please enter a valid URL with a domain extension"
    
    return True, url
