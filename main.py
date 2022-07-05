import glob
import time
import os
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

DOWNLOAD_PATH = '/Users/rodrigoramos/Downloads'

FILES_TO_MOVE = {
    'Documentos': {
        'docx',
        'doc'
    },
    'Instaladores': {
        'dmg'
    }

}


class Event(LoggingEventHandler):

    def on_modified(self, event):
        for folder in FILES_TO_MOVE:
            createOrFail(folder)
            for extension in FILES_TO_MOVE[folder]:
                files = glob.glob(DOWNLOAD_PATH + '/*.' + extension)
                for file in files:
                    try:
                        fileName = os.path.basename(os.path.normpath(file))
                        os.rename(file,
                                  DOWNLOAD_PATH + '/' + folder + '/' + fileName)
                    except:
                        print("erro!")


def main():
    event_handler = Event()

    observer = Observer()
    observer.schedule(
        event_handler, DOWNLOAD_PATH, recursive=True)

    # Start the observer
    observer.start()
    try:
        while True:
            # Set the thread sleep time
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def createOrFail(folder):
    if(os.path.isdir(DOWNLOAD_PATH + "/" + folder)):
        return
    os.makedirs(DOWNLOAD_PATH + "/" + folder)


if __name__ == "__main__":
    main()
