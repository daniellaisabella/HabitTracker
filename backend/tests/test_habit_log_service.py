from unittest.mock import patch
from datetime import date
import pytest
from backend.services import habit_log_service


# Test: ISO dato-string konverteres korrekt til date objekt og sendes til repo
@patch("backend.services.habit_log_service.habit_log_repository")
def test_log_habit_parses_date(mock_repo):
    habit_log_service.log_habit(1, "2026-05-26")
    mock_repo.create.assert_called_once_with(1, date(2026, 5, 26))


# Test: ugyldig dato-string kaster ValueError
def test_log_habit_invalid_date_raises():
    with pytest.raises(ValueError):
        habit_log_service.log_habit(1, "not-a-date")


# Test: manglende log_date (None) kaster ValueError
def test_log_habit_missing_date_raises():
    with pytest.raises(ValueError):
        habit_log_service.log_habit(1, None)


# Test: get_today delegerer til repo og returnerer boolean
@patch("backend.services.habit_log_service.habit_log_repository")
def test_get_today_delegates(mock_repo):
    mock_repo.get_today.return_value = True
    result = habit_log_service.get_today(1)
    mock_repo.get_today.assert_called_once_with(1)
    assert result is True


# Test: delete_today delegerer til repo
@patch("backend.services.habit_log_service.habit_log_repository")
def test_delete_today_delegates(mock_repo):
    habit_log_service.delete_today(1)
    mock_repo.delete_today.assert_called_once_with(1)


# Test: get_last_7_days delegerer til repo og returnerer liste
@patch("backend.services.habit_log_service.habit_log_repository")
def test_get_last_7_days_delegates(mock_repo):
    mock_repo.get_last_7_days.return_value = []
    result = habit_log_service.get_last_7_days(1)
    mock_repo.get_last_7_days.assert_called_once_with(1)
    assert result == []
