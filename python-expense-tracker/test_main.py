import json
from main import loadUser


def test_loadUser_existing(tmp_path, monkeypatch):
    # create a user.json in a temporary directory and chdir there
    user = {"name": "Alice", "role": "Engineer"}
    p = tmp_path / "user.json"
    p.write_text(json.dumps(user))
    monkeypatch.chdir(tmp_path)

    result = loadUser()

    assert "Welcome back, Alice" in result


def test_loadUser_creates(tmp_path, monkeypatch):
    # when user.json doesn't exist, loadUser should prompt and create it
    monkeypatch.chdir(tmp_path)

    inputs = iter(["Bob", "Manager"])
    monkeypatch.setattr('builtins.input', lambda prompt='': next(inputs))

    result = loadUser()

    assert "Welcome, Bob" in result

    p = tmp_path / "user.json"
    assert p.exists()
    data = json.loads(p.read_text())
    assert data == {"name": "Bob", "role": "Manager"}


def test_loadExpenses():
    pass 