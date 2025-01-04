from queue import SimpleQueue
from typing import Any
import numpy as np

class FeedProvider(SimpleQueue[np.full_like]):
    def __init__(self):
        super().__init__()
        self.__last__ = None

    def put(self, item: Any, block: bool = True, timeout: float | None = None) -> None:
        #if queue length is greater than 5, remove the oldest frame
        if self.qsize() > 5:
            self.get_nowait()
        
        return super().put(item, block, timeout)

    def get(self, block: bool = True, timeout: float | None = None) -> Any:
        
        if self.qsize() == 0 and not self.__last__ is None:
            return self.__last__
        else:
            self.__last__ = super().get(block, timeout)
            return self.__last__