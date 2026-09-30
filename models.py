from pydantic import BaseModel


class DocumentRequest(BaseModel):
    document_type: str
    parties: str
    terms: str
    dates: str


class DocumentResponse(BaseModel):
    content: str


class ExportRequest(BaseModel):
    content: str
    document_type: str