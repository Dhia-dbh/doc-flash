"""Public API routes."""

from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse

from doc_flash.api.dependencies import get_documentation_service
from doc_flash.api.schemas import CodePayload, DocumentedCodeResponse, GeneratedTestsResponse
from doc_flash.services.documentation_service import DocumentationService

router = APIRouter(prefix="/v1", tags=["documentation"])


@router.post("/document", response_model=DocumentedCodeResponse)
async def document_code(
    payload: CodePayload,
    service: DocumentationService = Depends(get_documentation_service),
) -> DocumentedCodeResponse:
    """Return code annotated with docstrings and inline comments."""
    documented = await service.document_code(payload.code)
    return DocumentedCodeResponse(documented_code=documented)


@router.post("/markdown", response_class=PlainTextResponse)
async def generate_markdown(
    payload: CodePayload,
    service: DocumentationService = Depends(get_documentation_service),
) -> PlainTextResponse:
    """Generate and stream a markdown description of the provided code."""
    markdown = await service.generate_markdown(payload.code)
    filename = payload.filename or "code_overview.md"
    return PlainTextResponse(
        content=markdown,
        media_type="text/markdown",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/tests", response_model=GeneratedTestsResponse)
async def generate_tests(
    payload: CodePayload,
    service: DocumentationService = Depends(get_documentation_service),
) -> GeneratedTestsResponse:
    """Generate pytest-style unit tests for the provided code."""
    tests = await service.generate_tests(payload.code)
    return GeneratedTestsResponse(tests_code=tests)
