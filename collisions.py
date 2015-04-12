import sfml as sf
from utils import intersects
from abc import ABCMeta, abstractmethod


class Collidable(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_bounding_rects(self):
        pass

    @abstractmethod
    def collide(self, other):
        pass


class CollisionManager(object):
    def __init__(self):
        self.objects = []

    def add(self, object):
        if not isinstance(object, Collidable):
            print 'Not a Collidable object'
            return

        self.objects.append(object)

    def update(self):
        for i in xrange(len(self.objects)):
            for j in xrange(i + 1, len(self.objects)):

                rects1 = self._to_iterable(self.objects[i].get_bounding_rects())
                rects2 = self._to_iterable(self.objects[j].get_bounding_rects())

                for a in rects1:
                    for b in rects2:
                        if intersects(a, b):
                            self.objects[i].collide(self.objects[j])
                            self.objects[j].collide(self.objects[i])

    @staticmethod
    def _to_iterable(object):
        if isinstance(object, sf.Rectangle):
            return [object]
        else:
            return list(object)



