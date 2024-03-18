import pytesseract

def ocr(image):
    # Open the image file
    image = image

    # Perform OCR using Tesseract
    text = pytesseract.image_to_string(image)

    # Return the extracted text
    return text

