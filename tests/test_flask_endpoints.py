import requests

BASE_URL = "http://localhost:5050"


def test_status():
    r = requests.get(f"{BASE_URL}/status")
    assert r.status_code == 200
    data = r.json()
    assert "flask" in data
    assert "localai" in data
    assert "watchdog" in data


def test_index():
    r = requests.get(f"{BASE_URL}/")
    assert r.status_code == 200
    assert "Flask" in r.text or "Status" in r.text


def test_kompetencer():
    r = requests.get(f"{BASE_URL}/kompetencer")
    assert r.status_code == 200
    assert "<h1>" in r.text or "<div" in r.text


def test_chat():
    r = requests.post(f"{BASE_URL}/chat", json={"message": "Hvad er mine styrker?"})
    assert r.status_code == 200
    assert "reply" in r.json()


def test_test_runner():
    r = requests.get(f"{BASE_URL}/test")
    assert r.status_code == 200
    assert "PASSED" in r.text or "FAILED" in r.text


def test_test_report():
    r = requests.get(f"{BASE_URL}/test-report")
    assert r.status_code == 200
    assert "<html" in r.text
