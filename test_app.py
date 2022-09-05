import pytest
import app
import json

@pytest.fixture
def client():
    print(app.app.config)
    app.app.config['TESTING'] = True
    app.app.testing = True
    print(app.app.config)
    test_client = app.app.test_client()
    yield test_client
    app.db.session.rollback()
    test_client.delete()

def test_get_employees(client):
    res = client.get('/employees')
    data = json.loads(res.data.decode('utf-8'))
    assert res.status == '200 OK'
    assert len(data) == 0
