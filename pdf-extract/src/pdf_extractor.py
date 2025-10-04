"""PDF text extraction functionality using PyMuPDF"""

import fitz  # PyMuPDF
from pathlib import Path
from typing import Optional
from .ocr_processor import OCRProcessor


class PDFExtractor:
    """Handles PDF text extraction with PyMuPDF"""

    MAX_FILE_SIZE_MB = 70
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
    MIN_TEXT_LENGTH = 50  # Minimum text length to consider page as text-based

    def __init__(self, ocr_processor: Optional[OCRProcessor] = None):
        """
        Initialize PDF extractor.

        Args:
            ocr_processor: Optional OCRProcessor instance for handling image-based PDFs
        """
        self.ocr_processor = ocr_processor or OCRProcessor()

    def validate_file(self, file_path: str) -> tuple[bool, Optional[str]]:
        """
        Validate PDF file exists and is within size limits.

        Args:
            file_path: Path to PDF file

        Returns:
            Tuple of (is_valid, error_message)
        """
        path = Path(file_path)

        if not path.exists():
            return False, f"File not found: {file_path}"

        if not path.is_file():
            return False, f"Path is not a file: {file_path}"

        file_size = path.stat().st_size
        if file_size > self.MAX_FILE_SIZE_BYTES:
            return False, f"File size ({file_size / 1024 / 1024:.2f} MB) exceeds limit of {self.MAX_FILE_SIZE_MB} MB"

        if file_size == 0:
            return False, "File is empty"

        return True, None

    def extract_text(
        self,
        file_path: str,
        pages: Optional[list[int]] = None,
        enable_ocr: bool = True
    ) -> dict:
        """
        Extract text from PDF file with optional OCR support.

        Args:
            file_path: Path to PDF file
            pages: Optional list of page numbers to extract (0-indexed). If None, extract all pages.
            enable_ocr: Whether to use OCR for image-based pages (default: True)

        Returns:
            Dictionary with:
                - file: filename
                - page_count: total number of pages
                - content: list of extracted text per page
                - ocr_used: boolean indicating if OCR was used
                - ocr_pages: list of page numbers where OCR was applied

        Raises:
            ValueError: If file validation fails
            Exception: If PDF processing fails
        """
        # Validate file
        is_valid, error_msg = self.validate_file(file_path)
        if not is_valid:
            raise ValueError(error_msg)

        try:
            # Open PDF
            doc = fitz.open(file_path)
            total_pages = len(doc)

            # Determine which pages to extract
            if pages is None:
                pages_to_extract = range(total_pages)
            else:
                # Validate page numbers
                invalid_pages = [p for p in pages if p < 0 or p >= total_pages]
                if invalid_pages:
                    doc.close()
                    raise ValueError(
                        f"Invalid page numbers {invalid_pages}. "
                        f"PDF has {total_pages} pages (0-{total_pages-1})"
                    )
                pages_to_extract = pages

            # Extract text from specified pages
            content = []
            ocr_pages = []
            ocr_used = False

            for page_num in pages_to_extract:
                page = doc[page_num]
                text = page.get_text().strip()

                # Check if page has sufficient text
                if len(text) < self.MIN_TEXT_LENGTH and enable_ocr:
                    # Try OCR if text is insufficient
                    ocr_text = self._extract_text_with_ocr(page, page_num)
                    if ocr_text:
                        text = ocr_text
                        ocr_used = True
                        ocr_pages.append(page_num)

                content.append(f"Page {page_num + 1}: {text}")

            doc.close()

            result = {
                "file": Path(file_path).name,
                "page_count": total_pages,
                "content": content,
                "ocr_used": ocr_used
            }

            if ocr_used:
                result["ocr_pages"] = ocr_pages

            return result

        except fitz.FileDataError as e:
            raise Exception(f"Corrupted or invalid PDF file: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")

    def _extract_text_with_ocr(self, page: fitz.Page, page_num: int) -> Optional[str]:
        """
        Extract text from a PDF page using OCR.

        Args:
            page: PyMuPDF page object
            page_num: Page number (for logging)

        Returns:
            Extracted text or None if OCR fails or is unavailable
        """
        if not self.ocr_processor.is_available():
            return None

        try:
            # Get images from the page
            image_list = page.get_images()

            if not image_list:
                # No images found, try rendering the page itself
                return self._ocr_rendered_page(page)

            # Extract text from all images on the page
            all_text = []
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = page.parent.extract_image(xref)
                image_bytes = base_image["image"]

                # Perform OCR on the image
                text = self.ocr_processor.extract_text_from_image(image_bytes)
                if text:
                    all_text.append(text)

            return "\n\n".join(all_text) if all_text else None

        except Exception:
            # If OCR fails, try rendering the page
            return self._ocr_rendered_page(page)

    def _ocr_rendered_page(self, page: fitz.Page) -> Optional[str]:
        """
        Render the entire page as an image and perform OCR.

        Args:
            page: PyMuPDF page object

        Returns:
            Extracted text or None if OCR fails
        """
        try:
            # Render page to image at 300 DPI for better OCR
            mat = fitz.Matrix(300 / 72, 300 / 72)
            pix = page.get_pixmap(matrix=mat)

            # Convert to PIL Image
            from PIL import Image
            import io

            img_data = pix.tobytes("png")
            image = Image.open(io.BytesIO(img_data))

            # Perform OCR
            text = self.ocr_processor.extract_text_from_pil_image(image)
            return text if text else None

        except Exception:
            return None
