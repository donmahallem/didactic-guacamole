from .sprite import Sprite
import typing


class Group(Sprite):

    def __init__(self,parent:typing.Self=None):
        super().__init__(parent)
        self._items = []

    def draw(self):
        for item in self._items:
            item.draw()

    def update(self, **kwargs):
        for item in self._items:
            item.update(*kwargs)

    def remove(self, item):
        if item in self._items:
            self._items.remove(item)

    def __len__(self):
        return len(self._items)
    def __iadd__(self,other):
        self.add(other)
        return self
    def __isub__(self,other):
        self.remove(other)
        return self
    def __contains__(self,other):
        return other in self._items

    @typing.overload
    def add(self, sprite: Sprite) -> None:
        pass

    @typing.overload
    def add(self, *sprite: list[Sprite]) -> None:
        pass

    def add(self, *sprites):
        if isinstance(sprites, typing.Tuple):
            for sprite in sprites:
                sprite.parent = self
                self._items.append(sprite)
        elif isinstance(sprites,Sprite):
            self._items.add(sprites)
        else:
            raise TypeError(f"{type(sprites)} is not of type Sprite")
