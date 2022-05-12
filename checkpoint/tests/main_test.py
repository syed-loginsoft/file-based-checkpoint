from pathlib import Path

# from checkpoint.main import FileCheckpointer
from ..main import FileCheckpointer

ptr = FileCheckpointer(str(Path(".").absolute().parent.absolute() / "data"))


def test_update():
    ptr.update("123", "value")
    assert True == Path(ptr.get_file_path("123")).exists()


def test_get():
    assert "value" == ptr.get("123")


def test_delete():
    ptr.delete("123")
    assert False == Path(ptr.get_file_path("123")).exists()