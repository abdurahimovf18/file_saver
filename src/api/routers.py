from fastapi import APIRouter, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse
import mimetypes

from src.api.dependency_injection import FILE_SERVICE
from src.exceptions.not_found_error import NotFoundError
from src.exceptions.validation_error import ValidationError

router = APIRouter()


@router.get("/{file_id}")
async def get_file(file_id: str, file_service: FILE_SERVICE) -> StreamingResponse:
    try:
        stream = file_service.stream_file(file_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=exc.message)
    media_type, _ = mimetypes.guess_type(file_id)
    media_type = media_type or "application/octet-stream"

    return StreamingResponse(
        content=stream,
        media_type="text/csv",
        headers={"Content-Disposition": f"inline; filename={file_id}"}
    )


@router.post("/upload_file")
async def upload_file(file: UploadFile, file_service: FILE_SERVICE) -> str:
    if file.filename is None:
        raise ValidationError(
            "Filename must be attached to the file."
        )
    file_id = await file_service.upload_file(file.filename, data=await file.read())
    return file_id
