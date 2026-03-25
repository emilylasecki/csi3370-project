import pytest
from app.group_manager import GroupManager

class MockSupabase:
    def table(self, name):
        return self
    def update(self, data):
        return self
    def eq(self, field, value):
        return self
    def execute(self):
        class Response:
            data = {"status": "success"}
        return Response()

@pytest.fixture
def manager():
    return GroupManager(MockSupabase())

def test_update_group_not_found(manager, monkeypatch):
    monkeypatch.setattr(manager, "get_group", lambda x: None) 
    with pytest.raises(Exception, match="Group not found"):
        manager.update_group(1, "Title", "blue", True, 1)


def test_update_group_unauthorized(manager, monkeypatch):
    monkeypatch.setattr(manager, "get_group", lambda x: {"user_id": 1}) 
    with pytest.raises(Exception, match="Unauthorized"):
        manager.update_group(1, "Title", "blue", True, -1)


def test_update_group_success(manager, monkeypatch):
    monkeypatch.setattr(manager, "get_group", lambda x: {"user_id": 1}) 
    response = manager.update_group(1, "Title", "blue", True, 1) 
    assert response.data["status"] == "success"