import json
import logging
from typing import List, Optional, Tuple

from app.models import Reminder
from app.database import db

logger = logging.getLogger(__name__)


class ReminderRepository:
    """Репозиторий для работы с напоминаниями"""

    @staticmethod
    def create(
        user_id: int,
        medication_name: str,
        dosage: str,
        time: str,
        days: List[int],
    ) -> Reminder:
        """Создать новое напоминание для конкретного пользователя"""
        try:
            if not isinstance(days, list):
                raise ValueError("Days must be a list of integers")

            days_json = json.dumps(days)

            # ВАЖНО: execute_query возвращает rowcount для non-SELECT
            insert_query = """
                INSERT INTO reminders (user_id, medication_name, dosage, reminder_time, days) 
                VALUES (%s, %s, %s, %s, %s)
            """
            db.execute_query(
                insert_query,
                (user_id, medication_name, dosage, time, days_json),
            )

            # Получаем только что созданную запись
            select_query = """
                SELECT * FROM reminders
                WHERE user_id = %s
                ORDER BY created_at DESC, id DESC
                LIMIT 1
            """
            rows = db.execute_query(select_query, (user_id,))
            if not rows:
                raise ValueError("Не удалось получить созданное напоминание")

            return Reminder.from_db(rows[0])

        except Exception as e:
            logger.error(f"Error creating reminder: {e}", exc_info=True)
            raise

    @staticmethod
    def get_filtered(
        user_id: int,
        search: Optional[str],
        day: Optional[int],
        is_active: Optional[bool],
        sort_by: str,
        sort_dir: str,
        page: int,
        page_size: int,
    ) -> Tuple[List[Reminder], int]:
        """Получить список напоминаний пользователя с фильтрацией/сортировкой/пагинацией"""
        try:
            params: List = [user_id]
            where_clauses = ["user_id = %s"]

            if search:
                where_clauses.append("LOWER(medication_name) LIKE LOWER(%s)")
                params.append(f"%{search}%")

            if day is not None:
                # days хранится в JSONB, элементы — числа
                where_clauses.append(
                    "%s = ANY (SELECT jsonb_array_elements_text(days)::int)"
                )
                params.append(day)

            if is_active is not None:
                where_clauses.append("is_active = %s")
                params.append(is_active)

            where_sql = " AND ".join(where_clauses)

            sort_column_map = {
                "time": "reminder_time",
                "created_at": "created_at",
            }
            sort_column = sort_column_map.get(sort_by, "reminder_time")
            sort_direction = "ASC" if sort_dir.lower() == "asc" else "DESC"

            offset = (page - 1) * page_size

            # Общее количество
            count_query = f"""
                SELECT COUNT(*) AS total
                FROM reminders
                WHERE {where_sql}
            """
            count_rows = db.execute_query(count_query, tuple(params))
            total = count_rows[0]["total"] if count_rows else 0

            # Данные страницы
            data_query = f"""
                SELECT * FROM reminders
                WHERE {where_sql}
                ORDER BY {sort_column} {sort_direction}
                LIMIT %s OFFSET %s
            """
            data_params = params + [page_size, offset]
            rows = db.execute_query(data_query, tuple(data_params))

            reminders = [Reminder.from_db(row) for row in rows]
            return reminders, total

        except Exception as e:
            logger.error(f"Error getting filtered reminders: {e}", exc_info=True)
            return [], 0

    @staticmethod
    def get_by_id(reminder_id: int, user_id: int) -> Optional[Reminder]:
        """Получить одно напоминание по id и пользователю"""
        try:
            rows = db.execute_query(
                "SELECT * FROM reminders WHERE id = %s AND user_id = %s",
                (reminder_id, user_id),
            )
            if not rows:
                return None
            return Reminder.from_db(rows[0])
        except Exception as e:
            logger.error(f"Error getting reminder by id: {e}", exc_info=True)
            return None

    @staticmethod
    def delete(reminder_id: int, user_id: int) -> bool:
        """Удалить напоминание пользователя"""
        try:
            result = db.execute_query(
                "DELETE FROM reminders WHERE id = %s AND user_id = %s",
                (reminder_id, user_id),
            )
            # result — это rowcount
            return bool(result) and result > 0
        except Exception as e:
            logger.error(f"Error deleting reminder: {e}", exc_info=True)
            return False

    @staticmethod
    def toggle(reminder_id: int, user_id: int) -> Optional[Reminder]:
        """Переключить флаг is_active для напоминания пользователя"""
        try:
            reminder = ReminderRepository.get_by_id(reminder_id, user_id)
            if not reminder:
                return None

            new_status = not reminder.is_active
            result = db.execute_query(
                "UPDATE reminders SET is_active = %s WHERE id = %s AND user_id = %s",
                (new_status, reminder_id, user_id),
            )
            if not result or result <= 0:
                return None

            return ReminderRepository.get_by_id(reminder_id, user_id)
        except Exception as e:
            logger.error(f"Error toggling reminder: {e}", exc_info=True)
            return None
