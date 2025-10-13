from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess, time

class ReloadHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if isinstance(event.src_path, str) and event.src_path.endswith((".py",)):
            print("Ændring opdaget – genstarter Flask...")
            subprocess.run(["pkill", "-f", "flask"])
            subprocess.Popen(["flask", "run"])

# Start overvågning
observer = Observer()
observer.schedule(ReloadHandler(), path=".", recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()