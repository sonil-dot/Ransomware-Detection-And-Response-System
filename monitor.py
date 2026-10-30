
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from database import save_event
import time


class RDRSEventHandler(FileSystemEventHandler):

    def on_created(self, event):
        if not event.is_directory:
            print(f"[CREATE] {event.src_path}")
            save_event("CREATE", event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            print(f"[MODIFY] {event.src_path}")
            save_event("MODIFY", event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"[DELETE] {event.src_path}")
            save_event("DELETE", event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            print(
                f"[RENAME/MOVE] {event.src_path} -> {event.dest_path}"
            )
            save_event(
                "RENAME",
                f"{event.src_path} -> {event.dest_path}"
            )


folder_to_watch = "./test_data"

event_handler = RDRSEventHandler()
observer = Observer()
observer.schedule(event_handler, folder_to_watch, recursive=True)

observer.start()

print(f"RDRS is monitoring: {folder_to_watch}")
print("Press Ctrl+C to stop.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
