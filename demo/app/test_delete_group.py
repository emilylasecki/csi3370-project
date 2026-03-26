import pytest
from app.group_manager import GroupManager

class MockSupabase:
    def table(self, name):
        return self
    def delete(self):
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

def test_delete_group_not_found(manager, monkeypatch):
    monkeypatch.setattr(manager, "get_group", lambda x: None) 
    with pytest.raises(Exception, match="Group not found"):
        manager.delete_group(1, 1)


def test_delete_group_unauthorized(manager, monkeypatch):
    monkeypatch.setattr(manager, "get_group", lambda x: {"user_id": 1}) 
    with pytest.raises(Exception, match="Unauthorized"):
        manager.delete_group(1, -1)


def test_delete_group_success(manager, monkeypatch):
    monkeypatch.setattr(manager, "get_group", lambda x: {"user_id": 1}) 
    response = manager.delete_group(1, 1) 
    assert response.data["status"] == "success"