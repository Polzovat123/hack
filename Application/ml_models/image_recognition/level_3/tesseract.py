import pytesseract
from PIL import Image

class InterfaceImageRecognition:

    def parse_pdf(self, pdf_image):
        """
        Parses the text from the provided pdf image.

        Args:
            pdf_image (str): The path to the image extracted from a PDF.

        Returns:
            str: The text detected in the image.
        """

        # Open the image
        image = Image.open(pdf_image)

        # Use Tesseract to do OCR on the image
        text = pytesseract.image_to_string(image)

        # Return the detected text
        return text