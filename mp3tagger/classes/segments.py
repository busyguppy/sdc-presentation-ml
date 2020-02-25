from typing import List, Tuple


class Segments:

    def __init__(self, segments: List[Tuple[str, str]]):
        self.segments = segments

    def __delitem__(self, key):
        del self.segments[key]

    def __getitem__(self, key):
        return self.segments[key]

    def __setitem__(self, key, value):
        self.segments[key] = value

    def __len__(self):
        return len(self.segments)

    def __str__(self):
        return ''.join([seg[1] for seg in self.segments])

if __name__ == '__main__':
    pass


