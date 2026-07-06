import queue
import threading
from downloader import download_video

task_queue = queue.Queue()


def worker(send_callback):
    while True:
        chat_id, url = task_queue.get()

        try:
            file_path = download_video(url)
            send_callback(chat_id, file_path)

        except Exception as e:
            send_callback(chat_id, None, error=str(e))

        task_queue.task_done()


def start_worker(send_callback):
    t = threading.Thread(target=worker, args=(send_callback,), daemon=True)
    t.start()