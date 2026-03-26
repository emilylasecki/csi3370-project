import pytest
from app.task_manager import TaskManager

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
    return TaskManager(MockSupabase())

def test_update_task_not_found(manager, monkeypatch):
    monkeypatch.setattr(manager, "get_task", lambda x: None) 
    with pytest.raises(Exception, match="Task not found"):
        manager.update_task(1, {"taskName": "New Name"}, 1)


def test_update_task_unauthorized(manager, monkeypatch):
    monkeypatch.setattr(manager, "get_task", lambda x: {"userID": 1}) 
    with pytest.raises(Exception, match="Unauthorized"):
        manager.update_task(1, {"taskName": "New Name"}, -1)


def test_update_task_success(manager, monkeypatch):
    monkeypatch.setattr(manager, "get_task", lambda x: {"userID": 1}) 
    response = manager.update_task(1, {"taskName": "New Name"}, 1) 
    assert response.data["status"] == "success"