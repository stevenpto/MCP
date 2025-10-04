"""Create a test PDF for testing the extraction tool"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_test_pdf(filename="test_medical_report.pdf"):
    """Create a sample medical report PDF for testing"""
    c = canvas.Canvas(filename, pagesize=letter)

    # Page 1
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "Medical Report - Patient: John Doe")
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, "Date: 2025-10-04")
    c.drawString(100, 700, "Patient ID: 12345")
    c.drawString(100, 670, "OCT Findings:")
    c.drawString(120, 650, "- Central macular thickness: 310 µm (right eye)")
    c.drawString(120, 630, "- Central macular thickness: 285 µm (left eye)")
    c.drawString(120, 610, "- Mild diabetic macular edema OS > OD")
    c.drawString(120, 590, "- No microaneurysms detected")
    c.showPage()

    # Page 2
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 750, "Prescription Details")
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, "Right Eye (OD): -2.00 SPH")
    c.drawString(100, 700, "Left Eye (OS): -2.25 SPH")
    c.drawString(100, 670, "Recommendation: Progressive lenses")
    c.drawString(100, 640, "Follow-up: 6 months")
    c.showPage()

    c.save()
    print(f"Created test PDF: {filename}")

if __name__ == "__main__":
    create_test_pdf()
