import unicodedata
from typing import List

from mp3tagger.classes.segments_feature_vector import SegmentsFV
from mp3tagger.classes.segmentizer import Segmentizer
from mp3tagger.classes.segments import Segments


class TitleInfo:
    """
    用來儲存資料收集、處理過程中各種資訊，方便處理、傳遞。包含YouTube標題、歌手、歌曲等資訊。

    Example:
        ...

    Attributes:
        title (str): YouTube影片標題或是mp3檔案名稱。
        song_title (str):
        feature_vectors (List[FeatureVector]):
    """

    title = str
    artist = str
    song_title = str
    feature_vectors = SegmentsFV

    def __init__(self):
        self.title = ''
        self.__segments = None
        self.artist = ''
        self.song_title = ''
        self.feature_vectors = []

    def __hash__(self):
        return hash(self.artist.lower() + ' ' + self.song_title.lower())

    def __eq__(self, other):
        if self.artist == other.artist and self.song_title == other.song_title:
            return True
        return False
