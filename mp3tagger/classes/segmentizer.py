import unicodedata

from mp3tagger.classes.segments import Segments
from mp3tagger.classes.punctuations import *


class Segmentizer:

    def char_segmentation(self, title: str) -> Segments:
        return Segments([(unicodedata.category(c), c) for c in title])

    def word_segmentation(self, segs: Segments) -> Segments:
        # ('Lu', 'm'), ('Ll', 'a')相鄰兩個小寫英文字母應該合併成('Lstr','ma')
        # ('Lo', '張'), ('Lo', '三')相鄰兩個字母unicode category 'other'應該合併成('Lo', '張三')
        ll = ['Lu', 'Ll', 'Lstr']
        i = 0
        while i < len(segs) - 1:
            t1, s1 = segs[i]
            t2, s2 = segs[i + 1]
            if t1 in ll and t2 in ll:
                segs[i:i + 2] = [('Lstr', s1 + s2)]
                continue
            elif t1 == t2:
                if segs[i][0] == 'Po':
                    i += 1
                    continue
                segs[i:i + 2] = [(t1, s1 + s2)]
                continue
            # space separator，用空白字元取代
            elif t1 == 'Zs':
                segs[i] = (t1, ' ')
            # 任何connector/dash punctuation或是在自訂的dash裡面，都用-取代
            # Pc: _, ‿, ︳, ﹍, ＿
            elif t1 in ['Pc', 'Pd']:
                segs[i] = ('Pd', '-')
            i += 1

        # 移除歌曲標題中不必要的圾垃資訊
        i = 0
        while i < len(segs):
            if segs[i][1].lower() in stopwords:
                del segs[i]
                if i-1 >= 0 and i < len(segs) and segs[i - 1][0] == 'Zs' and segs[i][0] == 'Zs':
                    del segs[i]
                    # continue
                continue
            i += 1
        return segs


    def in_dash_quotes(self, c):
        return any(c in s for s in dq)

    def phrase_segmentation(self, title: str) -> Segments:
        segs = self.word_segmentation(self.char_segmentation(title))
        ls = ['Lu', 'Ll', 'Lstr']    # Latin string
        i = 0
        while i < len(segs):
            # <Lstr> + ' ' + 'X' + ' ' + <Lstr>
            # if i + 4 < len(segs) and segs[i][0] in ls and segs[i+2][1].lower() in connectors \
            #         and segs[i+4][0] in ls:
            #     segs[i:i+5] = [('Lstr', segs[i][1] + ' ' + segs[i+2][1] + ' ' + segs[i+4][1])]
            # # <Lo> + ' ' + 'X' + ' ' + <Lo>
            # elif i + 4 < len(segs) and segs[i][0] == 'Lo' and segs[i+2][1].lower() in connectors \
            #         and segs[i+4][0] == 'Lo':
            #     segs[i:i+5] = [('Lo', segs[i][1] + ' ' + segs[i+2][1] + ' ' + segs[i+4][1])]
            # thinkin' 這類文字應該合併
            if i + 2 < len(segs) and segs[i][0] == 'Lstr' and segs[i + 1][1] == "'" \
                     and segs[i+2][0] == 'Zs':
                segs[i:i + 2] = [('Lstr', segs[i][1] + "'")]
            # 兩個英文字串中間夾個空白，合併成('Lstr', <英文字串><空白><英文字串>)
            elif i+2 < len(segs) and segs[i][0] in ls and segs[i+1][1] == ' ' \
                    and segs[i+2][0] in ls:

                # 避免feat被併入左邊字串: <英文><空白><feat><.>
                if i + 3 < len(segs) and segs[i+2][1].lower() == 'feat' \
                        and segs[i+3][1] == '.':
                    i += 1
                    continue
                segs[i:i+3] = [('Lstr', segs[i][1] + ' ' + segs[i+2][1])]
            # that's 這類文字應該合併
            elif i+2 < len(segs) and segs[i][0] in ls and segs[i+1][1] == "'"\
                    and segs[i+2][0] in ls:
                segs[i:i+3] = [('Lstr', segs[i][1] + "'" + segs[i+2][1])]
            # 去掉分隔字元/括號前空白，除了 '以外，因為 that's
            elif i+1 < len(segs) and segs[i][0] == 'Zs' and segs[i+1][1] != "'"\
                    and self.in_dash_quotes(segs[i+1][1]):
                segs[i:i + 2] = [segs[i + 1]]
            # 去掉分隔字元/括號後空白
            elif i + 1 < len(segs) and segs[i][1] != "'" and self.in_dash_quotes(segs[i][1]) \
                    and segs[i + 1][0] == 'Zs':
                segs[i:i + 2] = [segs[i]]
            # 去掉,前空白
            elif i + 1 < len(segs) and segs[i][1] == ' ' \
                    and segs[i + 1][1] == ',':
                segs[i:i + 2] = [segs[i+1]]
            elif i+1 < len(segs) and segs[i][1].lower() == 'feat' \
                    and segs[i+1][1] == '.':
                segs[i:i+2] = [(segs[i+1][0], segs[i][1] + segs[i+1][1])]
            else:
                i += 1

        return segs

if __name__ == '__main__':
    title = 'Cassette 卡式帶樂團 - 某日 (Official Music Video)'
    s = Segmentizer()
    sg = s.phrase_segmentation(title)
    print(sg)
