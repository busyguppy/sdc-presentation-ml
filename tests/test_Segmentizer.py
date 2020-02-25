
import unittest

from mp3tagger.classes.segmentizer import Segmentizer


class TestSegmentizer(unittest.TestCase):

    def test_char_segmentation(self):
        s = 'Cassette 卡式帶樂團 - 某日 (某日)'
        segments = Segmentizer().char_segmentation(s)
        assert len(segments) == len(s)
        for seg in segments:
            assert isinstance(seg, tuple)
            assert len(seg) == 2
            assert isinstance(seg[0], str)
            assert isinstance(seg[1], str)

    def test_word_segmentation(self):
        title = 'Cassette 卡式帶樂團 - 某日 (某日)'
        st = Segmentizer()
        segments = st.word_segmentation(st.char_segmentation(title))
        assert ('Lstr', 'Cassette') in segments
        assert ('Lo', '卡式帶樂團') in segments

    def test_phase_segmentation(self):
        st = Segmentizer()

        title = 'Fire On The Mountain Lyrics - Rob Thomas'
        segments = st.phrase_segmentation(title)
        assert ('Lstr', 'Lyrics') not in segments

        title = 'Cassette, 卡式帶樂團 - 某日 (某日)'
        segments = st.phrase_segmentation(title)
        assert ('Lstr', 'Cassette') in segments
        assert ('Lo', '卡式帶樂團') in segments

        # 測試英文字串能否連接
        # title = ' " Cassette id  ", 卡式帶樂團 - 某日 ( 某日)'
        # segments = st.phrase_segmentation(title)
        # assert ('Lstr', 'Cassette id') in segments

        # 測試 " ( - 前後空白是否正確去掉
        title = ' )     '
        segments = st.phrase_segmentation(title)
        assert (str(segments) == ')')

        # 測試 ' 是否會去掉兩邊空白，應該不會才對
        title = "gg ' gg"
        segments = st.phrase_segmentation(title)
        assert (str(segments) == "gg ' gg")

        # 測試 that's 是否正常
        title = "/ that's )"
        segments = st.phrase_segmentation(title)
        assert ('Lstr', "that's") in segments

        # thinkin' 這類文字應該合併
        title = " ( thinkin' ww)"
        segments = st.phrase_segmentation(title)
        assert ('Lstr', "thinkin' ww") in segments

        # 測試連接詞是否能連接前後英文字串
        # title = ' band  &  band, 卡式帶樂團 - 某日 ( 某日)'
        # segments = st.phrase_segmentation(title)
        # assert ('Lstr', 'band & band') in segments

        # 測試連接詞是否能連接前後中文字串
        # title = '鍾一憲 x 麥貝夷《勾手指尾》MV'
        # segments = st.phrase_segmentation(title)
        # assert ('Lo', '鍾一憲 x 麥貝夷') in segments

        # 測試連接詞x在沒前後詞彙情況下是否會併入鄰近segment
        # title = ' band X 某日 x band - 某日 ( 某日)'
        # segments = st.phrase_segmentation(title)
        # assert ('Lstr', 'band X') in segments
        # assert ('Lstr', 'x band') in segments

        # 測試feat.是否成為單一segment
        title = ' band  &  band, 卡式帶樂團 AAA feat. JJJ - 某日 ( 某日)'
        segments = st.phrase_segmentation(title)
        assert ('Po', 'feat.') in segments


if __name__ == '__main__':
    unittest.main()