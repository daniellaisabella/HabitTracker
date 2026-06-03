from unittest.mock import patch
import pytest
from backend.services import habit_service

# Test: tomt navn kaster ValueError
@patch("backend.services.habit_service.habit_repository")
def test_create_raises_on_empty_name(mock_repo):
    with pytest.raises(ValueError):
        habit_service.create("")


