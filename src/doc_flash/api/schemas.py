"""Request and response schemas."""

from pydantic import BaseModel, Field


class CodePayload(BaseModel):
    code: str = Field(..., description="Raw source code to be documented.")
    filename: str | None = Field(
        default=None,
        description="Optional filename to use when returning markdown content.",
    )


class DocumentedCodeResponse(BaseModel):
    documented_code: str


class GeneratedTestsResponse(BaseModel):
    tests_code: str
