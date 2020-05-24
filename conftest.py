import pytest


@pytest.fixture(autouse=True)
def no_requests(request, monkeypatch):
    # Original code from: https://github.com/mvantellingen/python-zeep/blob/master/tests/conftest.py
    if request.node.get_closest_marker("requests"):
        return

    def func(*args, **kwargs):
        pytest.fail("External connections not allowed during tests. Please mock requests.")

    monkeypatch.setattr("socket.socket", func)
