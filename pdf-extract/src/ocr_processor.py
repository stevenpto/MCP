"""OCR processing functionality using Tesseract"""

import io
import os
from pathlib import Path
from typing import Optional
from PIL import Image


class OCRProcessor:
    """Handles OCR processing for image-based PDFs using Tesseract"""

    def __init__(self):
        """Initialize OCR processor"""
        self._setup_tesseract_path()
        self._tesseract_available = self._check_tesseract()

    def _setup_tesseract_path(self):
        """Set up Tesseract path for common Windows installations"""
        try:
            import pytesseract

            # Common Tesseract installation paths on Windows
            common_paths = [
                r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
                r"C:\Tesseract-OCR\tesseract.exe",
            ]

            # Check if tesseract is already in PATH
            try:
                pytesseract.get_tesseract_version()
                return  # Already configured
            except Exception:
                pass

            # Try common paths
            for path in common_paths:
                if Path(path).exists():
                    pytesseract.pytesseract.tesseract_cmd = path
                    return

        except Exception:
            pass

    def _check_tesseract(self) -> bool:
        """
        Check if Tesseract is available on the system.

        Returns:
            True if Tesseract is available, False otherwise
        """
        try:
            import pytesseract
            # Try to get version to verify Tesseract is installed
            pytesseract.get_tesseract_version()
            return True
        except Exception:
            return False

    def is_available(self) -> bool:
        """
        Check if OCR functionality is available.

        Returns:
            True if Tesseract is installed and available
        """
        return self._tesseract_available

    def extract_text_from_image(
        self,
        image_data: bytes,
        language: str = "eng"
    ) -> str:
        """
        Extract text from image data using OCR.

        Args:
            image_data: Raw image bytes
            language: Tesseract language code (default: 'eng' for English)

        Returns:
            Extracted text from image

        Raises:
            RuntimeError: If Tesseract is not available
            Exception: If OCR processing fails
        """
        if not self._tesseract_available:
            raise RuntimeError(
                "Tesseract OCR is not installed. Please install Tesseract to use OCR features. "
                "Installation instructions: https://github.com/tesseract-ocr/tesseract#installing-tesseract"
            )

        try:
            import pytesseract

            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data))

            # Convert to RGB if necessary (some PDFs have CMYK or other formats)
            if image.mode not in ('RGB', 'L'):
                image = image.convert('RGB')

            # Perform OCR
            text = pytesseract.image_to_string(image, lang=language)

            return text.strip()

        except Exception as e:
            raise Exception(f"Failed to extract text from image using OCR: {str(e)}")

    def extract_text_from_pil_image(
        self,
        image: Image.Image,
        language: str = "eng"
    ) -> str:
        """
        Extract text from PIL Image object using OCR.

        Args:
            image: PIL Image object
            language: Tesseract language code (default: 'eng' for English)

        Returns:
            Extracted text from image

        Raises:
            RuntimeError: If Tesseract is not available
            Exception: If OCR processing fails
        """
        if not self._tesseract_available:
            raise RuntimeError(
                "Tesseract OCR is not installed. Please install Tesseract to use OCR features. "
                "Installation instructions: https://github.com/tesseract-ocr/tesseract#installing-tesseract"
            )

        try:
            import pytesseract

            # Convert to RGB if necessary
            if image.mode not in ('RGB', 'L'):
                image = image.convert('RGB')

            # Perform OCR
            text = pytesseract.image_to_string(image, lang=language)

            return text.strip()

        except Exception as e:
            raise Exception(f"Failed to extract text from image using OCR: {str(e)}")

    def get_installation_message(self) -> str:
        """
        Get installation instructions for Tesseract.

        Returns:
            Installation instructions string
        """
        return """
Tesseract OCR is not installed on your system.

To enable OCR functionality, install Tesseract:

Windows:
  1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
  2. Run the installer
  3. Add Tesseract to PATH or set pytesseract.pytesseract.tesseract_cmd

macOS:
  brew install tesseract

Linux (Ubuntu/Debian):
  sudo apt-get install tesseract-ocr

Linux (Fedora):
  sudo dnf install tesseract

After installation, restart your MCP server.
"""
