from unittest.mock import patch
from datetime import datetime
import pytest
from backend.services import habit_service
from backend.models.habit import Habit


@patch("backend.services.habit_service.habit_repository")
def test_create_returns_habit(mock_repo):
    mock_habit = Habit(id=1, name="Sport", created_at=datetime.now())
    mock_repo.create.return_value = mock_habit
    result = habit_service.create("Sport")
    mock_repo.create.assert_called_once_with("Sport")
    assert result is mock_habit


def test_create_raises_on_empty_name():
    with pytest.raises(ValueError):
        habit_service.create("")


@patch("backend.services.habit_service.habit_repository")
def test_get_all_delegates(mock_repo):
    mock_repo.get_all.return_value = []
    result = habit_service.get_all()
    mock_repo.get_all.assert_called_once()
    assert result == []


@patch("backend.services.habit_service.habit_repository")
def test_delete_delegates(mock_repo):
    habit_service.delete(42)
    mock_repo.delete.assert_called_once_with(42)
