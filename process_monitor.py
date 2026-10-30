
import psutil
from database import save_process


def collect_process_metadata():
    for process in psutil.process_iter(
        ["pid", "name", "username", "memory_info"]
    ):
        try:
            info = process.info
            memory = info["memory_info"]

            if memory:
                memory_mb = round(
                    memory.rss / (1024 * 1024), 2
                )
            else:
                memory_mb = 0.0

            pid = info["pid"]
            name = info["name"] or "Unknown"
            username = info["username"] or "Unknown"

            print("-" * 40)
            print(f"PID: {pid}")
            print(f"Name: {name}")
            print(f"Username: {username}")
            print(f"Memory: {memory_mb} MB")

            save_process(pid, name, username, memory_mb)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue


if __name__ == "__main__":
    collect_process_metadata()
