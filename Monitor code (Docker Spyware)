import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Script started")


import time
import os
from watchdog.observers import Observer 
from watchdog.events import FileSystemEventHandler

MONITORED_FOLDER = "/app/monitored_folder"

class ImageMonitorHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        
        file_path = event.src_path
        if file_path.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
            print(f"[ALERT] New image detected: {file_path}")

            # Simulating exfiltration by logging instead of actually sending data
            with open("/app/log.txt", "a") as log_file:
                log_file.write(f"Image detected: {file_path}\n")

if __name__ == "__main__":
    if not os.path.exists(MONITORED_FOLDER):
        os.makedirs(MONITORED_FOLDER)

    event_handler = ImageMonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, path=MONITORED_FOLDER, recursive=False)

    print("[INFO] Monitoring folder for new images...")
    observer.start()
    
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
