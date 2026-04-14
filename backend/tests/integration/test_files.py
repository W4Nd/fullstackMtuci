# tests/integration/test_files.py
import pytest
from fastapi import status

@pytest.mark.skip
def test_upload_file(client, auth_headers, reminder, monkeypatch):
    # Мокаем функцию сохранения файла
    async def mock_save_file(file, user_id, reminder_id):
        return {"file_id": 1, "url": "http://fake"}
    monkeypatch.setattr("app.services.file_service.save_uploaded_file", mock_save_file)

    files = {"file": ("test.txt", b"hello world", "text/plain")}
    response = client.post(f"/api/v1/reminders/{reminder['id']}/files", files=files, headers=auth_headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["file_id"] == 1

@pytest.mark.skip
def test_download_file(client, auth_headers, reminder, file_fixture):
    response = client.get(f"/api/v1/files/{file_fixture['id']}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "application/octet-stream"  # или конкретный тип

@pytest.mark.skip
def test_download_other_user_file(client, auth_headers, other_user_file):
    response = client.get(f"/api/v1/files/{other_user_file['id']}", headers=auth_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN