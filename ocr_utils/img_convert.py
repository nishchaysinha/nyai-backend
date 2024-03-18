import base64
from PIL import Image
from io import BytesIO

def base64_to_image(base64_string):
    # Remove the data URL prefix if it exists
    if base64_string.startswith("data:image"):
        base64_string = base64_string.split(",")[1]

    # Decode base64 string to bytes
    image_bytes = base64.b64decode(base64_string)

    # Convert bytes to PIL Image
    image = Image.open(BytesIO(image_bytes))

    return image

