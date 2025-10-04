
---

# 📄 PRD: Document Ingestion Suite (MCP Tools for PDF Extraction & Summarization)

## 1. Objective

Develop a **Document Ingestion Suite** consisting of two MCP tools:

1. **`extract_text_from_pdf`** — extracts raw text and metadata from PDFs.
2. **`summarize_pdf_section`** — summarizes extracted text into concise, context-aware insights.

Together, these tools allow the AI agent to:

* Parse medical/administrative PDFs (patient reports, prescriptions, OCT/fundus reports).
* Summarize extracted text into structured outputs.
* Support both general and context-driven summarization.

---

## 2. Scope

### In-Scope

* Extracting text from PDFs with embedded text.
* Returning per-page content and metadata.
* Optional summarization during extraction.
* Independent summarization of extracted text.
* JSON output usable by LLMs.

### Out-of-Scope

* OCR for image-only/scanned PDFs.
* Image interpretation (retinal scans, fundus photos).
* Formatting preservation (fonts, tables, images).

---

## 3. Tools Specification

### 3.1 Tool: `extract_text_from_pdf`

**Description**
Extracts text and metadata from a PDF file, with optional inline summarization.

**Parameters**

```json
{
  "type": "object",
  "properties": {
    "file_path": {
      "type": "string",
      "description": "The local or accessible path to the PDF file."
    },
    "pages": {
      "type": "array",
      "items": { "type": "integer" },
      "description": "Optional list of page numbers to extract (0-indexed). If omitted, extract all pages."
    },
    "summarize": {
      "type": "boolean",
      "description": "Whether to summarize the extracted text.",
      "default": false
    },
    "context": {
      "type": "string",
      "description": "Optional context for summarization (e.g., 'focus on prescriptions', 'highlight OCT findings')."
    }
  },
  "required": ["file_path"]
}
```

**Response Format**

```json
{
  "file": "patient_oct_report.pdf",
  "page_count": 2,
  "content": [
    "Page 1: Patient: John Doe. OCT findings: Central macular thickness 310 µm...",
    "Page 2: Impression: Mild diabetic macular edema OS > OD..."
  ],
  "summary": "Optional: Summarized text if summarize=true"
}
```

---

### 3.2 Tool: `summarize_pdf_section`

**Description**
Summarizes raw extracted PDF text into concise, structured insights.

**Parameters**

```json
{
  "type": "object",
  "properties": {
    "pdf_text": {
      "type": "string",
      "description": "The raw text content extracted from the PDF."
    },
    "context": {
      "type": "string",
      "description": "Optional guidance for summarization (e.g., 'focus on prescriptions', 'highlight abnormal OCT findings')."
    }
  },
  "required": ["pdf_text"]
}
```

**Response Format**

```json
{
  "summary": "Summarized text based on pdf_text and context",
  "focus": "Optional: Detected focus or theme (e.g., 'Prescription details')"
}
```

---

## 4. Implementation Requirements

* **Language**: Python
* **Libraries**:

  * [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) → for text extraction.
  * Summarization can be:

    * LLM-based (preferred, pass context + text to agent).
    * Simple extractive summarizer fallback (`gensim`, `sumy`).

### Functions

```python
def extract_text_from_pdf(
    file_path: str, 
    pages: list[int] = None, 
    summarize: bool = False, 
    context: str = None
) -> dict:
    ...

def summarize_pdf_section(
    pdf_text: str, 
    context: str = None
) -> dict:
    ...
```

**Steps for Extraction**

1. Open PDF with PyMuPDF.
2. Extract text per page (all or specified pages).
3. Return JSON with file metadata, page count, and text content.
4. If `summarize=true`, call summarizer with extracted text and `context`.
5. Catch errors (invalid path, corrupted PDF).

**Steps for Summarization**

1. Accept text input.
2. Apply summarization algorithm.
3. If `context` provided, bias summary toward it.
4. Return JSON with `summary` and optional `focus`.

---

## 5. Example Use Cases

### Case 1 — Extraction Only

**Request**

```json
{
  "file_path": "reports/patient_oct_2025.pdf"
}
```

**Response**

```json
{
  "file": "reports/patient_oct_2025.pdf",
  "page_count": 2,
  "content": [
    "Page 1: Patient John Doe, OCT findings...",
    "Page 2: Impression: Mild diabetic macular edema..."
  ]
}
```

---

### Case 2 — Extraction with Summarization

**Request**

```json
{
  "file_path": "reports/patient_oct_2025.pdf",
  "summarize": true,
  "context": "highlight OCT findings and impressions"
}
```

**Response**

```json
{
  "file": "reports/patient_oct_2025.pdf",
  "page_count": 2,
  "content": [
    "Page 1: Patient John Doe, OCT findings...",
    "Page 2: Impression: Mild diabetic macular edema..."
  ],
  "summary": "OCT indicates early diabetic macular edema with microaneurysms; OS less affected than OD."
}
```

---

### Case 3 — Independent Summarization

**Request**

```json
{
  "pdf_text": "Patient: John Doe. Prescription: -2.00 OD, -2.25 OS. Recommended progressive lenses.",
  "context": "focus on prescriptions"
}
```

**Response**

```json
{
  "summary": "Patient John Doe has mild myopia; progressive lenses recommended.",
  "focus": "Prescription details"
}
```

---

## 6. Non-Functional Requirements

* Must process a 20-page PDF in <2 seconds on average hardware.
* Must support PDFs up to 50 MB in size.
* Must return UTF-8 encoded JSON.
* Must handle empty/invalid input gracefully.
* Summarization must complete within 2 seconds for text inputs <10,000 characters.

---

## 7. Future Extensions

* Add OCR fallback for scanned PDFs.
* Support additional formats (DOCX, TXT, image files).
* Add ontology tagging (ICD/SNOMED).
* Add patient-facing plain-language summaries.

---

✅ With this PRD, your coding agent can build the **Document Ingestion Suite** as a clean package with **two interoperable tools** — one for extraction, one for summarization.

---

Would you like me to also draft a **sample workflow diagram (ASCII or image)** showing how the agent + MCP tools + LLM interact end-to-end (User → LLM → MCP tools → LLM → User)?
