from queue import SimpleQueue
from typing import Any

class CameraFeed(SimpleQueue):
    def __init__(self):
        super().__init__()
        self._shared = False

    def share(self):
        self._shared = True

    def unshare(self):
        self._shared = False

    def is_shared(self):
        return self._shared
    
    # def put(self, item: Any, block: bool = True, timeout: float | None = None) -> None:
    #     print("Putting item in shared store")
    #     return super().put(item, block, timeout)

    