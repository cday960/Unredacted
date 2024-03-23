from .document import Document
import threading


class DocQueue:
    def __init__(self):
        self.docs: list[Document] = []
        self.lock = threading.Lock()

    def enqueue(self, doc: Document) -> None:
        """Add an item to the end of the queue."""
        with self.lock:
            self.docs.append(doc)

    def dequeue(self) -> Document:
        """Remove and return the first item in the queue."""
        ret_val = None
        with self.lock:
            if len(self.docs) > 0:
                ret_val = self.docs.pop(0)
        return ret_val

    def size(self):
        """Return the number of items in the queue."""
        with self.lock:
            return len(self.docs)
