
import sqlite3
import database


def test_save_event_and_process(tmp_path, monkeypatch):
    db_path = tmp_path / "test_rdrs.db"
    original_connect = sqlite3.connect

    def temporary_connect(*args, **kwargs):
        return original_connect(str(db_path), **kwargs)

    monkeypatch.setattr(database.sqlite3, "connect", temporary_connect)

    database.create_database()
    database.save_event("MODIFY", "./test_data/sample.txt")
    database.save_process(1234, "test.exe", "testuser", 12.5)

    connection = original_connect(str(db_path))
    cursor = connection.cursor()

    cursor.execute("SELECT event_type, file_path FROM events")
    assert cursor.fetchone() == ("MODIFY", "./test_data/sample.txt")

    cursor.execute(
        "SELECT pid, process_name, username, memory_mb FROM processes"
    )
    assert cursor.fetchone() == (1234, "test.exe", "testuser", 12.5)

    connection.close()
