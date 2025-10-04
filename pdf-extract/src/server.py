"""MCP Server for PDF Extraction and Summarization"""

from mcp.server.fastmcp import FastMCP
from typing import Optional
from .pdf_extractor import PDFExtractor
from .summarizer import TextSummarizer

# Initialize FastMCP server
mcp = FastMCP("pdf-extract")

# Initialize extractors
pdf_extractor = PDFExtractor()
text_summarizer = TextSummarizer()


@mcp.tool()
def extract_text_from_pdf(
    file_path: str,
    pages: Optional[list[int]] = None,
    summarize: bool = False,
    context: Optional[str] = None,
    max_sentences: Optional[int] = None,
    enable_ocr: bool = True
) -> dict:
    """
    Extract text and metadata from a PDF file, with optional OCR and summarization.

    Args:
        file_path: The local or accessible path to the PDF file
        pages: Optional list of page numbers to extract (0-indexed). If omitted, extract all pages
        summarize: Whether to summarize the extracted text (default: False)
        context: Optional context for summarization (e.g., 'focus on prescriptions', 'highlight OCT findings')
        max_sentences: Maximum sentences in summary (auto-calculated if None: 30% of text, min 5, max 15)
        enable_ocr: Use OCR for image-based pages (default: True, requires Tesseract installation)

    Returns:
        Dictionary containing:
            - file: filename
            - page_count: total number of pages in PDF
            - content: list of extracted text per page
            - ocr_used: boolean indicating if OCR was used
            - ocr_pages: (optional) list of page numbers where OCR was applied
            - summary: (optional) summarized text if summarize=True
            - focus: (optional) detected focus if summarize=True and context provided
    """
    try:
        # Extract text from PDF with optional OCR
        result = pdf_extractor.extract_text(
            file_path=file_path,
            pages=pages,
            enable_ocr=enable_ocr
        )

        # Add summarization if requested
        if summarize:
            # Combine all page content for summarization
            full_text = "\n\n".join(result["content"])
            summary_result = text_summarizer.summarize(
                text=full_text,
                context=context,
                max_sentences=max_sentences
            )
            result["summary"] = summary_result["summary"]
            if summary_result.get("focus"):
                result["focus"] = summary_result["focus"]

        return result

    except ValueError as e:
        return {"error": str(e), "type": "validation_error"}
    except Exception as e:
        return {"error": str(e), "type": "processing_error"}


@mcp.tool()
def summarize_pdf_section(
    pdf_text: str,
    context: Optional[str] = None,
    max_sentences: Optional[int] = None
) -> dict:
    """
    Summarize raw extracted PDF text into concise, structured insights.

    Args:
        pdf_text: The raw text content extracted from the PDF
        context: Optional guidance for summarization (e.g., 'focus on prescriptions', 'highlight abnormal OCT findings')
        max_sentences: Maximum sentences in summary (auto-calculated if None: 30% of text, min 5, max 15)

    Returns:
        Dictionary containing:
            - summary: Summarized text based on pdf_text and context
            - focus: (optional) Detected focus or theme (e.g., 'Prescription Details')
    """
    try:
        if not pdf_text or not pdf_text.strip():
            return {
                "error": "pdf_text cannot be empty",
                "type": "validation_error"
            }

        # Summarize the text
        result = text_summarizer.summarize(
            text=pdf_text,
            context=context,
            max_sentences=max_sentences
        )
        return result

    except Exception as e:
        return {"error": str(e), "type": "processing_error"}


# Entry point for running the server
if __name__ == "__main__":
    mcp.run()
