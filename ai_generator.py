import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def generate_document(document_type, parties, terms, effective_date):

    demo_mode = os.getenv("DEMO_MODE", "true").lower() == "true"

    if demo_mode or not GEMINI_API_KEY:

        return f"""
{document_type.upper()}

Effective Date: {effective_date}

PARTIES
{parties}

AGREEMENT

This {document_type} is entered into between the parties
identified above and is effective from {effective_date}.

TERMS AND CONDITIONS

{terms}

GENERAL PROVISIONS

1. The parties agree to the terms stated in this document.
2. Any changes should be made in writing.
3. The document should be reviewed before signing.

SIGNATURES

Party 1: __________________________

Signature: ________________________

Date: _____________________________


Party 2: __________________________

Signature: ________________________

Date: _____________________________
""".strip()

    try:
        from google import genai

        client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        prompt = f"""
Create a professional draft legal document.

Document Type: {document_type}

Effective Date: {effective_date}

Parties:
{parties}

Terms:
{terms}

Use clear professional legal language.
Include headings and signature sections.
Do not invent information.
"""

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        return response.text.strip()

    except Exception:
        return generate_document(
            document_type,
            parties,
            terms,
            effective_date,
        )