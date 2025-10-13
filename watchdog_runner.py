from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time
import os

WATCH_PATHS = ["./app", "./tests", "./data"]  # mapper du vil overvåge

class TestRunner(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return
        print(f"Ændring opdaget: {event.src_path}")
        subprocess.run(["pytest", "--tb=short", "--disable-warnings"])

if __name__ == "__main__":
    event_handler = TestRunner()
    observer = Observer()
    for path in WATCH_PATHS:
        if os.path.exists(path):
            observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print("🔁 Watchdog kører – overvåger ændringer...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()