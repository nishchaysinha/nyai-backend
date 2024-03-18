import pytesseract
import requests
import os

def ocr(image):
    # Open the image file
    image = image

    # Perform OCR using Tesseract
    text = pytesseract.image_to_string(image)

    # Return the extracted text
    return text

def ocr_api(image_base64):
    url = "https://api.ocr.space/parse/image"
    headers = {
    "apikey": "helloworld"
    }
    data = {
        "base64Image": image_base64,
        "language": "eng",
        "isOverlayRequired": "false"
    }
    response = requests.post(url, headers=headers, data=data)

    # The response will be in JSON format, so you can convert it to a Python dictionary using .json()
    response_dict = response.json()
    return response_dict['ParsedResults'][0]['ParsedText']

