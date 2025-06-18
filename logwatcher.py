"""
tail_log_watchdog.py
--------------------
• Asks for the full path of a log file.
• Uses watchdog to listen for *modify* (and *move*) events on that file.
• Keeps an internal byte‑offset so it never rereads what it has already sent.
• Prints each newly‑appended line to the console (replace `process()` with
  whatever you need—e.g. upload to server).

Requires:  pip install watchdog
Tested on: Python 3.8+
"""

import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def handle_new_log_lines(lines: list[str]):
    """This function will be called with each batch of new lines."""
    print("🔔 New log lines received:")
    for line in lines:
        print("→", line)


class TailHandler(FileSystemEventHandler):
    def __init__(self, target: Path):
        self.target = target
        self.offset = 0
        self._sync_offset()
        self.last_check = time.time()
        self.check_interval = 0.1  # Check every 100ms even without events

    def _sync_offset(self):
        """Start tailing from the current end of file."""
        try:
            self.offset = self.target.stat().st_size
        except FileNotFoundError:
            self.offset = 0

    def _read_new_lines(self):
        """Read and decode new lines added to the log."""
        try:
            with self.target.open("rb") as f:
                f.seek(self.offset)
                data = f.read()
                self.offset = f.tell()
                if data:
                    return data.decode(errors="ignore").splitlines()
        except FileNotFoundError:
            pass
        return []

    def check_for_changes(self):
        """Actively check for new content regardless of events"""
        current_time = time.time()
        if current_time - self.last_check >= self.check_interval:
            self.last_check = current_time
            new_lines = self._read_new_lines()
            if new_lines:
                handle_new_log_lines(new_lines)

    def on_modified(self, event):
        try:
            if Path(str(event.src_path)) == self.target:
                self.check_for_changes()
        except Exception:
            pass  # Handle any path conversion errors gracefully


def main():
    file_path = Path(input("Enter path to log file: ").strip()).expanduser().resolve()

    if not file_path.exists():
        print(f"⚠️  File {file_path} does not exist. Waiting for it to be created...")

    handler = TailHandler(file_path)
    observer = Observer()
    observer.schedule(handler, path=str(file_path.parent), recursive=False)
    observer.start()

    print(f"✅ Tailing log: {file_path}\nPress Ctrl+C to stop.")
    try:
        while True:
            handler.check_for_changes()  # Actively check for changes
            time.sleep(0.1)  # Small sleep to prevent high CPU usage
    except KeyboardInterrupt:
        print("\n⏹️  Stopping...")
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
