import json
from main import loadUser, loadExpenses


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


def test_loadExpenses_existing(tmp_path, monkeypatch, capsys):
    expenses = [
        {"description": "Groceries", "amount": 120, "category": "Food"},
        {"description": "Train", "amount": 30, "category": "Transport"},
    ]
    p = tmp_path / "expenseData.json"
    p.write_text(json.dumps(expenses))
    monkeypatch.chdir(tmp_path)

    loadExpenses()

    captured = capsys.readouterr()
    assert "Loading expenses..." in captured.out
    assert "Groceries" in captured.out
    assert "TOTAL SPENT: 150" in captured.out


def test_loadExpenses_missing(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    loadExpenses()

    captured = capsys.readouterr()
    assert "No expense found." in captured.out
    assert (tmp_path / "expenseData.json").exists()
    assert json.loads((tmp_path / "expenseData.json").read_text()) == []