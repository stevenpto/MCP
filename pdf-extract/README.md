# PDF Extract MCP Server

Document Ingestion Suite - MCP server for PDF extraction and summarization using the FAST MCP framework.

## Features

- **Extract text from PDFs**: Parse text-based PDFs with PyMuPDF
- **OCR Support**: Extract text from scanned/image-based PDFs using Tesseract OCR
- **Summarize content**: Generate concise summaries with context-aware guidance
- **Large file support**: Handle PDFs up to 70 MB
- **High performance**: Process text-based PDFs in under 2 seconds
- **Auto-detection**: Automatically detects and uses OCR when pages lack embedded text

## Tools

### 1. `extract_text_from_pdf`

Extracts text and metadata from PDF files with optional OCR and inline summarization.

**Parameters:**
- `file_path` (string, required): Path to the PDF file
- `pages` (array of integers, optional): Specific page numbers to extract (0-indexed). If omitted, extracts all pages
- `summarize` (boolean, optional): Whether to summarize extracted text (default: false)
- `context` (string, optional): Context for summarization (e.g., "focus on prescriptions")
- `max_sentences` (integer, optional): Maximum sentences in summary (auto-calculated if not provided)
- `enable_ocr` (boolean, optional): Use OCR for image-based pages (default: true)

**Returns:**
```json
{
  "file": "document.pdf",
  "page_count": 5,
  "content": ["Page 1: ...", "Page 2: ..."],
  "ocr_used": true,
  "ocr_pages": [2, 3],
  "summary": "Optional summary if summarize=true"
}
```

### 2. `summarize_pdf_section`

Summarizes extracted PDF text into structured insights.

**Parameters:**
- `pdf_text` (string, required): Raw text content from PDF
- `context` (string, optional): Guidance for summarization focus

**Returns:**
```json
{
  "summary": "Concise summary of the text",
  "focus": "Detected theme (optional)"
}
```

## Installation

### 1. Install Python Dependencies

```bash
pip install pytesseract Pillow PyMuPDF mcp sumy nltk
```

Or use requirements file:
```bash
pip install -r requirements.txt
```

### 2. Install Tesseract OCR (Required for OCR features)

**Windows:**
1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer (recommended: C:\Program Files\Tesseract-OCR)
3. Add Tesseract to PATH, or the MCP server will auto-detect common locations

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

**Linux (Fedora):**
```bash
sudo dnf install tesseract
```

### 3. Verify Installation

```bash
tesseract --version
```

**Note:** OCR features are optional. If Tesseract is not installed, the server will work for text-based PDFs but will skip OCR for image-based pages.

## Usage

### Running the Server

```bash
python -m src.server
```

Or use with MCP client by adding to your MCP settings:

```json
{
  "mcpServers": {
    "pdf-extract": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "C:\\Projects\\mcp\\pdf-extract"
    }
  }
}
```

### Example Usage

**Extract all pages (with auto OCR):**
```python
extract_text_from_pdf(file_path="reports/medical_report.pdf")
```

**Extract scanned/image PDF with OCR:**
```python
extract_text_from_pdf(
    file_path="reports/scanned_prescription.pdf",
    enable_ocr=True
)
```

**Extract specific pages with summarization:**
```python
extract_text_from_pdf(
    file_path="reports/oct_findings.pdf",
    pages=[0, 1, 2],
    summarize=True,
    context="highlight OCT findings and impressions",
    max_sentences=10
)
```

**Disable OCR for faster processing:**
```python
extract_text_from_pdf(
    file_path="reports/text_only.pdf",
    enable_ocr=False
)
```

**Independent summarization:**
```python
summarize_pdf_section(
    pdf_text="Patient: John Doe. Prescription: -2.00 OD, -2.25 OS...",
    context="focus on prescriptions"
)
```

## Use Cases

- **Scanned Medical Records**: OCR and extract text from scanned patient reports, lab results
- **Mixed Documents**: Handle PDFs with both embedded text and scanned pages
- **Prescriptions**: Extract text from handwritten or printed prescription images
- **Administrative Documents**: Process forms, consent documents (scanned or digital)
- **Research Papers**: Extract specific sections and generate focused summaries

## Technical Details

- **Language**: Python 3.10+
- **Framework**: FAST MCP
- **PDF Library**: PyMuPDF (fitz)
- **OCR Engine**: Tesseract (via pytesseract)
- **Image Processing**: Pillow (PIL)
- **Summarization**: Extractive summarization with sumy and NLTK
- **Max File Size**: 70 MB
- **Performance**:
  - Text-based PDFs: <2s for 20-page PDFs
  - OCR-based PDFs: 1-3s per page at 300 DPI

## Limitations

- OCR requires Tesseract installation (optional, but recommended)
- OCR accuracy depends on scan quality (90-95% for clear scans)
- Handwritten text may have lower OCR accuracy
- Does not preserve formatting, tables, or complex layouts
- Summarization is extractive (not generative)
- OCR processing is slower than text extraction (1-3s per page)

## Future Extensions

- ✅ ~~OCR support for scanned PDFs~~ (Completed)
- Multi-language OCR support (currently English only)
- Table extraction and structured output
- Additional document formats (DOCX, TXT, images)
- Medical ontology tagging (ICD/SNOMED codes)
- Image interpretation for medical scans (fundus photos, OCT images)
- GPU acceleration for faster OCR processing

## License

MIT
