from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from blackhole import start, getPath

class BlackholeHandler(FileSystemEventHandler):
    def __init__(self, is_radarr):
        super().__init__()
        self.is_radarr = is_radarr
        self.path_name = getPath(is_radarr, create=True)

    def on_created(self, event=None):
        if not event or (not event.is_directory and event.src_path.lower().endswith((".torrent", ".magnet"))):
            start(self.is_radarr)

if __name__ == "__main__":
    print("Watching blackhole")

    radarr_handler = BlackholeHandler(is_radarr=True)
    sonarr_handler = BlackholeHandler(is_radarr=False)

    radarr_handler.on_created()
    sonarr_handler.on_created()

    radarr_observer = Observer()
    radarr_observer.schedule(radarr_handler, radarr_handler.path_name)

    sonarr_observer = Observer()
    sonarr_observer.schedule(sonarr_handler, sonarr_handler.path_name)

    try:
        radarr_observer.start()
        sonarr_observer.start()
    except KeyboardInterrupt:
        radarr_observer.stop()
        sonarr_observer.stop()

    radarr_observer.join()
    sonarr_observer.join()
