from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import time

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, tracked_path: Path):
        self.tracked_path = tracked_path
        self.previous_snapshot = self.snapshot()

    def snapshot(self):
        return set(p.relative_to(self.tracked_path) for p in self.tracked_path.rglob("*"))

    def on_any_event(self, event):
        current_snapshot = self.snapshot()
        added = current_snapshot - self.previous_snapshot
        removed = self.previous_snapshot - current_snapshot

        if added:
            print("🟢 Added:")
            for item in sorted(added):
                print("  +", item)
        if removed:
            print("🔴 Removed:")
            for item in sorted(removed):
                print("  -", item)

        self.previous_snapshot = current_snapshot


def main():
    path_str = input("Enter the folder path to monitor: ").strip()
    # path_str = "./testfolder".strip()
    watch_path = Path(path_str).expanduser().resolve()

    if not watch_path.exists() or not watch_path.is_dir():
        print("❌ Invalid folder path.")
        return

    print(f"👀 Watching: {watch_path}")
    event_handler = ChangeHandler(watch_path)
    observer = Observer()
    observer.schedule(event_handler, path=str(watch_path), recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping watcher...")
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
