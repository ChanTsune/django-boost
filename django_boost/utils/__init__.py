class Loop:
    def __init__(self, iterable):
        self.iterable = enumerate(iterable)
        self.length = len(iterable)

    def __iter__(self):
        return self

    def __next__(self):
        i, item = next(self.iterable)
        # Shortcuts for current loop iteration number.
        self.counter0 = i
        self.counter = i + 1
        # Reverse counter iteration numbers.
        self.revcounter = self.length - i
        self.revcounter0 = self.length - i - 1
        # Boolean values designating first and last times through loop.
        self.first = (i == 0)
        self.last = (i == self.length - 1)
        return self, item


def loop(iterable):
    return Loop(iterable)


def isiterable(obj):
    try:
        iter(obj)
    except TypeError:
        return False
    return True
