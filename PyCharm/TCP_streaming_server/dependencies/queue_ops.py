from multiprocessing import Queue
from queue import Empty


def lossy_enqueue(q: Queue, data):
    r = None

    if q.full():
        try:
            r = q.get_nowait()
        except Empty:
            pass

    q.put(data)
    return r
