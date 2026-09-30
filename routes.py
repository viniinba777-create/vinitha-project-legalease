from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse, StreamingResponse
from io import BytesIO

from .models import DocumentRequest, DocumentResponse, ExportRequest
from .ai_generator import generate_document


router = APIRouter()


@router.post("/generate", response_model=DocumentResponse)
def generate(request: DocumentRequest):

    if not request.parties.strip():
        raise HTTPException(
            status_code=400,
            detail="Parties are required.",
        )

    if not request.terms.strip():
        raise HTTPException(
            status_code=400,
            detail="Terms are required.",
        )

    document = generate_document(
        request.document_type,
        request.parties,
        request.terms,
        request.effective_date,
    )

    return DocumentResponse(
        document=document,
        document_type=request.document_type,
        mode="demo",
    )


@router.post("/export/txt")
def export_txt(request: ExportRequest):

    return PlainTextResponse(
        request.document,
        media_type="text/plain",
        headers={
            "Content-Disposition":
                'attachment; filename="legalease_document.txt"'
        },
    )


@router.post("/export/docx")
def export_docx(request: ExportRequest):

    try:
        from docx import Document

        document = Document()

        title = document.add_paragraph()
        title.alignment = 1

        run = title.add_run(
            "LegalEase\nLegal Document"
        )
        run.bold = True
        run.font.size = 160000  # 16pt in EMU

        for line in request.document.splitlines():

            line = line.strip()

            if not line:
                document.add_paragraph()
                continue

            paragraph = document.add_paragraph(line)

            if line.isupper() and len(line) < 100:
                for run in paragraph.runs:
                    run.bold = True

        output = BytesIO()
        document.save(output)
        output.seek(0)

        return StreamingResponse(
            output,
            media_type=(
                "application/vnd.openxmlformats-"
                "officedocument.wordprocessingml.document"
            ),
            headers={
                "Content-Disposition":
                    'attachment; filename="legalease_document.docx"'
            },
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"DOCX export failed: {exc}",
        )


@router.post("/export/pdf")
def export_pdf(request: ExportRequest):

    try:
        from fpdf import FPDF

        pdf = FPDF()
        pdf.set_auto_page_break(
            auto=True,
            margin=15,
        )
        pdf.add_page()

        pdf.set_font(
            "Helvetica",
            "B",
            16,
        )

        pdf.cell(
            0,
            10,
            "LegalEase - Legal Document",
            new_x="LMARGIN",
            new_y="NEXT",
            align="C",
        )

        pdf.ln(5)

        pdf.set_font(
            "Helvetica",
            "",
            11,
        )

        for line in request.document.splitlines():

            if not line.strip():
                pdf.ln(5)
                continue

            pdf.multi_cell(
                0,
                7,
                line,
            )

        pdf_bytes = pdf.output()

        return StreamingResponse(
            BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition":
                    'attachment; filename="legalease_document.pdf"'
            },
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"PDF export failed: {exc}",
        )