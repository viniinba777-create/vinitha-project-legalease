import os
from dotenv import load_dotenv
from google import genai

# Load variables from .env
load_dotenv()


class GeminiDocumentGenerator:
    def __init__(self):
        # Get Gemini API key from .env
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. Please add it to your .env file."
            )

        # Create Gemini client
        self.client = genai.Client(api_key=api_key)

    def generate_document(self, document_type, parties, terms, dates):
        """
        Generate a legal document using Gemini.
        """

        prompt = f"""
You are an AI legal document drafting assistant.

Create a professional draft legal document based ONLY on the
information provided by the user.

Document type:
{document_type}

Parties:
{parties}

Terms and conditions:
{terms}

Effective date:
{dates}

Instructions:
- Clearly identify the parties.
- Include the provided terms and conditions.
- Include the effective date.
- Use formal legal language.
- Organize the document with clear headings and sections.
- Do not invent important facts that were not provided.
- Do not claim that the document is legal advice.
- Return only the document text.
"""

        # Use the current Gemini Interactions API
        response = self.client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt
        )

        return response.output_text