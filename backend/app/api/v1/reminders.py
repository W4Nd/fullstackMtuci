import logging
from enum import Enum
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from pydantic import BaseModel, Field

from app.api.v1.auth import get_current_user
from app.repositories.reminder_repository import ReminderRepository
from app.models import Reminder

logger = logging.getLogger(__name__)
router = APIRouter()


class CreateReminder(BaseModel):
    medication_name: str = Field(..., min_length=1, max_length=100)
    dosage: str = Field(..., min_length=1, max_length=50)
    time: str = Field(..., pattern=r"^\d{2}:\d{2}$")
    days: List[int] = Field(..., min_items=1)


class UpdateReminder(BaseModel):
    medication_name: Optional[str] = Field(None, min_length=1, max_length=100)
    dosage: Optional[str] = Field(None, min_length=1, max_length=50)
    time: Optional[str] = Field(None, pattern=r"^\d{2}:\d{2}$")
    days: Optional[List[int]] = Field(None, min_items=1)
    is_active: Optional[bool] = None


class ReminderSortField(str, Enum):
    time = "time"
    created_at = "created_at"


class SortDirection(str, Enum):
    asc = "asc"
    desc = "desc"


@router.post("/")
async def create_reminder(
    data: CreateReminder,
    current_user: dict = Depends(get_current_user),
):
    """Создать напоминание для текущего пользователя"""
    try:
        reminder = ReminderRepository.create(
            user_id=current_user["user_id"],
            medication_name=data.medication_name,
            dosage=data.dosage,
            time=data.time,
            days=data.days,
        )
        return reminder.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Create reminder error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Ошибка сервера при создании напоминания")


@router.get("/")
async def get_reminders(
    current_user: dict = Depends(get_current_user),
    search: Optional[str] = Query(None, min_length=1, max_length=100),
    day: Optional[int] = Query(None, ge=0, le=6),
    is_active: Optional[bool] = Query(None),
    sort_by: ReminderSortField = Query(ReminderSortField.time),
    sort_dir: SortDirection = Query(SortDirection.asc),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    """Получить список напоминаний текущего пользователя с фильтром/сортировкой/пагинацией"""
    reminders, total = ReminderRepository.get_filtered(
        user_id=current_user["user_id"],
        search=search,
        day=day,
        is_active=is_active,
        sort_by=sort_by.value,
        sort_dir=sort_dir.value,
        page=page,
        page_size=page_size,
    )

    return {
        "items": [r.to_dict() for r in reminders],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get("/{reminder_id}")
async def get_reminder(
    reminder_id: int = Path(..., ge=1),
    current_user: dict = Depends(get_current_user),
):
    """Получить одно напоминание пользователя"""
    reminder = ReminderRepository.get_by_id(reminder_id, current_user["user_id"])
    if not reminder:
        raise HTTPException(status_code=404, detail="Напоминание не найдено")
    return reminder.to_dict()


@router.delete("/{reminder_id}")
async def delete_reminder(
    reminder_id: int = Path(..., ge=1),
    current_user: dict = Depends(get_current_user),
):
    """Удалить напоминание пользователя"""
    success = ReminderRepository.delete(reminder_id, current_user["user_id"])
    if not success:
        raise HTTPException(status_code=404, detail="Напоминание не найдено")
    return {"message": "Напоминание удалено"}


@router.post("/{reminder_id}/toggle")
async def toggle_reminder(
    reminder_id: int = Path(..., ge=1),
    current_user: dict = Depends(get_current_user),
):
    """Переключить активность напоминания пользователя"""
    reminder = ReminderRepository.toggle(reminder_id, current_user["user_id"])
    if not reminder:
        raise HTTPException(status_code=404, detail="Напоминание не найдено")
    return reminder.to_dict()
