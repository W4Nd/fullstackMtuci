from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from pydantic import BaseModel, Field

from app.api.v1.auth import get_current_user
from app.services.rbac_service import RBACService
from app.repositories.reminder_repository import ReminderRepository
from app.database import db

router = APIRouter()


def get_rbac_service():
    return RBACService()


class FileUploadRequest(BaseModel):
    file_name: str = Field(..., min_length=1, max_length=255)
    content_type: str = Field(..., min_length=1, max_length=100)
    size: int = Field(..., gt=0)


MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_TYPES = {"application/pdf", "image/jpeg", "image/png"}


@router.post("/{reminder_id}/files/upload-url")
async def get_upload_url(
    reminder_id: int = Path(..., ge=1),
    data: FileUploadRequest = ...,
    current_user: dict = Depends(get_current_user),
    rbac: RBACService = Depends(get_rbac_service),
):
    """Получить presigned URL для загрузки файла (5.1, 5.2, 5.4)"""
    if not rbac.has_permission(
        rbac.get_user_roles(current_user["user_id"]), "reminder:update_own"
    ):
        raise HTTPException(403, "Недостаточно прав")

    reminder = ReminderRepository.get_by_id(reminder_id, current_user["user_id"])
    if not reminder:
        raise HTTPException(404, "Reminder not found")

    if data.size > MAX_FILE_SIZE:
        raise HTTPException(400, "File too large")
    if data.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, "Unsupported file type")

    file_key = f"reminders/{current_user['user_id']}/{reminder_id}/{data.file_name}"
    presigned_url = "https://example.com/presigned"  

    return {
        "upload_url": presigned_url,
        "file_key": file_key,
    }


class FileConfirmRequest(BaseModel):
    file_key: str
    file_name: str
    content_type: Optional[str] = None
    size: Optional[int] = None


@router.post("/{reminder_id}/files/confirm")
async def confirm_file(
    reminder_id: int,
    data: FileConfirmRequest,
    current_user: dict = Depends(get_current_user),
    rbac: RBACService = Depends(get_rbac_service),
):
    """Подтвердить загрузку и сохранить метаданные (5.1, 5.3)"""
    if not rbac.has_permission(
        rbac.get_user_roles(current_user["user_id"]), "reminder:update_own"
    ):
        raise HTTPException(403, "Недостаточно прав")

    reminder = ReminderRepository.get_by_id(reminder_id, current_user["user_id"])
    if not reminder:
        raise HTTPException(404, "Reminder not found")

    query = """
        INSERT INTO reminder_files (reminder_id, user_id, file_key, file_name, content_type, size)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
    """
    rows = db.execute_query(
        query,
        (
            reminder_id,
            current_user["user_id"],
            data.file_key,
            data.file_name,
            data.content_type,
            data.size,
        ),
    )
    file_id = rows[0]["id"]

    return {"id": file_id}


@router.get("/{reminder_id}/files")
async def list_files(
    reminder_id: int,
    current_user: dict = Depends(get_current_user),
    rbac: RBACService = Depends(get_rbac_service),
):
    """Список файлов для напоминания"""
    if not rbac.has_permission(
        rbac.get_user_roles(current_user["user_id"]), "reminder:read_own"
    ):
        raise HTTPException(403, "Недостаточно прав")

    reminder = ReminderRepository.get_by_id(reminder_id, current_user["user_id"])
    if not reminder:
        raise HTTPException(404, "Reminder not found")

    rows = db.execute_query(
        "SELECT id, file_name, content_type, size, created_at FROM reminder_files WHERE reminder_id = %s AND user_id = %s",
        (reminder_id, current_user["user_id"]),
    )
    return rows


@router.get("/files/{file_id}/download-url")
async def get_download_url(
    file_id: int,
    current_user: dict = Depends(get_current_user),
    rbac: RBACService = Depends(get_rbac_service),
):
    """Получить presigned URL для скачивания файла (5.2)"""
    if not rbac.has_permission(
        rbac.get_user_roles(current_user["user_id"]), "reminder:read_own"
    ):
        raise HTTPException(403, "Недостаточно прав")

    rows = db.execute_query(
        "SELECT * FROM reminder_files WHERE id = %s AND user_id = %s",
        (file_id, current_user["user_id"]),
    )
    if not rows:
        raise HTTPException(404, "File not found")
    file = rows[0]

    presigned_url = "https://example.com/presigned-download"  

    return {"download_url": presigned_url}


@router.delete("/files/{file_id}")
async def delete_file(
    file_id: int,
    current_user: dict = Depends(get_current_user),
    rbac: RBACService = Depends(get_rbac_service),
):
    """Удаление файла и очистка метаданных (5.3, 6)"""
    if not rbac.has_permission(
        rbac.get_user_roles(current_user["user_id"]), "reminder:update_own"
    ):
        raise HTTPException(403, "Недостаточно прав")

    rows = db.execute_query(
        "SELECT * FROM reminder_files WHERE id = %s AND user_id = %s",
        (file_id, current_user["user_id"]),
    )
    if not rows:
        raise HTTPException(404, "File not found")
    file = rows[0]


    db.execute_query(
        "DELETE FROM reminder_files WHERE id = %s AND user_id = %s",
        (file_id, current_user["user_id"]),
    )

    return {"message": "File deleted"}
