# class to store different types of overlays, in order to add overlay to list it must have draw method
# on init empty list is created and then latest items can be added and removed, supports __enter__ and __exit__

class Overlays:
    def __init__(self):
        self.__overlays__ = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__overlays__ = []

    def add(self, overlay):
        if not hasattr(overlay, 'draw'):
            raise ValueError("Overlay must have a draw method")
        self.__overlays__.append(overlay)

    def remove(self, overlay):
        self.__overlays__.remove(overlay)

    def draw(self, frame):
        for overlay in self.__overlays__:
            overlay.draw(frame)