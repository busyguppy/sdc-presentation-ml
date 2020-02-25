from typing import List, Tuple


class SegmentsFV:

    def __init__(self, fvs: List[dict]):
        self.content = fvs

    def __str__(self) -> str:
        return ''.join([d['str'] for d in self.content])

    def __delitem__(self, key):
        del self.content[key]

    def __getitem__(self, key):
        return self.content[key]

    def __setitem__(self, key, value):
        self.content[key] = value

    def __len__(self):
        return len(self.content)

