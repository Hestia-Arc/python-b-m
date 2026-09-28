import json
from main import loadUser, loadExpenses, addExpense, deleteExpense, viewAllExpenses, calByCategory


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


def test_addExpense_success(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    answers = iter(["50", "Food", "Groceries"])
    monkeypatch.setattr('builtins.input', lambda prompt='': next(answers))

    result = addExpense()

    assert "Groceries added" in result
    data = json.loads((tmp_path / "expenseData.json").read_text())
    assert len(data) == 1
    assert data[0]["amount"] == 50
    assert data[0]["category"] == "Food"
    assert data[0]["description"] == "Groceries"
    assert "createdAt" in data[0]


def test_addExpense_reprompts_on_empty_category_and_description(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    answers = iter(["20", "", "Transport", "", "Bus ticket"])
    monkeypatch.setattr('builtins.input', lambda prompt='': next(answers))

    result = addExpense()

    captured = capsys.readouterr()
    assert "Category cannot be empty" in captured.out
    assert "Description cannot be empty" in captured.out
    assert "Bus ticket added" in result


def test_deleteExpense_success(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    expenses = [
        {"id": "a1", "description": "Groceries", "amount": 120, "category": "Food"},
        {"id": "b2", "description": "Train", "amount": 30, "category": "Transport"},
    ]
    (tmp_path / "expenseData.json").write_text(json.dumps(expenses))

    result = deleteExpense(0)

    assert "Groceries deleted" in result
    saved = json.loads((tmp_path / "expenseData.json").read_text())
    assert len(saved) == 1
    assert saved[0]["description"] == "Train"


def test_deleteExpense_invalid_index(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    expenses = [
        {"id": "a1", "description": "Groceries", "amount": 120, "category": "Food"},
    ]
    (tmp_path / "expenseData.json").write_text(json.dumps(expenses))

    result = deleteExpense(99)

    assert result == "Expense not found."
    saved = json.loads((tmp_path / "expenseData.json").read_text())
    assert len(saved) == 1


def test_viewAllExpenses_returns_data(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    expenses = [
        {"description": "Groceries", "amount": 120, "category": "Food"},
        {"description": "Train", "amount": 30, "category": "Transport"},
    ]
    (tmp_path / "expenseData.json").write_text(json.dumps(expenses))

    result = viewAllExpenses()

    assert result == expenses
    assert len(result) == 2


def test_calByCategory_returns_total_for_matching_category(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    expenses = [
        {"description": "Groceries", "amount": 120, "category": "Food"},
        {"description": "Lunch", "amount": 40, "category": "Food"},
        {"description": "Train", "amount": 30, "category": "Transport"},
    ]
    (tmp_path / "expenseData.json").write_text(json.dumps(expenses))

    result = calByCategory("food")

    assert result == "Total for food: 160"


def test_calByCategory_no_match(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    expenses = [
        {"description": "Groceries", "amount": 120, "category": "Food"},
    ]
    (tmp_path / "expenseData.json").write_text(json.dumps(expenses))

    result = calByCategory("travel")

    assert result == "No expenses found for category: travel."