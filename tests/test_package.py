import jamstack


def test_version_is_exposed() -> None:
    assert jamstack.__version__
