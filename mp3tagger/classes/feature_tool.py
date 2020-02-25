import logging

from mp3tagger.classes.segments_feature_vector import SegmentsFV
from mp3tagger.classes.segmentizer import Segmentizer
from mp3tagger.classes.punctuations import *


class FeatureTool:

    def __init__(self):
        pass

    def __word_in_list(self, word: str, word_list: list):
        for s in word_list:
            if word.lower() == s:
                return True
        return False

    def feature_vectors(self, title: str) -> SegmentsFV:
        st = Segmentizer()
        segs = st.phrase_segmentation(title)

        strlen = 0
        Lo_cnt = 0
        fvs = []        # a list of FeatureVector extracted from title string
        '''
        為了統一起見，只要是left就不含當前token，right才包含。

        str:              字串內容，例如Alison Lau, 劉卓衹
        tag:              Lstr: Alison Lau, Lo: 劉卓衹，由group, word, phrase而來
        i_seg:            第幾個分隔好的字串token, 第一個為0。
        str_len_left:     前面所有token字串長度，不包含自己。。
        seg_len:          目前token字串長度。
        left_lo_seg_cnt:  到目前為止中文token個數，不包含自己。
        '''
        for i, (t, s) in enumerate(segs):
            fv = dict(  # title每個phrase作為一個feature vector
                tag=t, str=s, i_seg=i, str_len_left=strlen, seg_len=len(s)
            )
            fv['left_lo_seg_cnt'] = Lo_cnt
            if t == 'Lo':
                Lo_cnt += 1

            if not s.lower() in stopwords:
                fvs.append(fv)
                strlen += len(s)

        '''
        title_len:        歌曲標題字串長度
        right_seg_cnt:    包括自己，後面有幾個segment
        right_seg_len:    包括自己，後面segment總字串長度
        right_lo_seg_cnt: 包括自己，後面有多少個中文segment
        '''
        for v in fvs:
            v.update({
                'title_len': strlen,
                'right_seg_cnt': len(fvs) - v['i_seg'],
                'right_seg_length': strlen - v['str_len_left']
            })
            v['right_lo_seg_cnt'] = Lo_cnt - v['left_lo_seg_cnt']


        qpos = {}
        for key in quotes + ['-']:
            qpos[key] = []

        for v in fvs:
            if v['tag'] == 'Pd':
                qpos['-'].append(v['i_seg'])
            else:
                for quote in quotes:
                    # 在目前token中找到任一quote字元
                    if v['str'] in quote:
                        # 標記括號出現token index
                        # {'()': [8, 12], '[]': [], '《》': [5, 7], '【】': [], '（）': [], '“”': [], "''": [], '""': [], '-': []}
                        qpos[quote].append(v['i_seg'])
                        break

        '''
        i_slot_between_dash:    在第幾個i構成的間隔
        in_quote:               True/False，是否被某種引號包起來
        quote_type:             引號種類
        '''
        default_value = 100
        for v in fvs:
            try:
                for i, index in enumerate(qpos['-']):
                    if v['str'] == '-':
                        v['i_slot_between_dash'] = default_value
                        break
                    elif v['i_seg'] > index:
                        continue
                    else:
                        v['i_slot_between_dash'] = i
                        break
                if v.get('i_slot_between_dash') == None:
                    v['i_slot_between_dash'] = len(qpos['-'])
            except ValueError:
                v['i_slot_between_dash'] = default_value

            for quote in quotes:
                if not qpos[quote]:
                    continue
                in_quote = [True for i, j in zip(qpos[quote][::2], qpos[quote][1::2])
                            if i < v['i_seg'] < j]
                v['in_quote'] = bool(in_quote)
                v['quote_type'] = quote if v['in_quote'] else ''
            if v.get('in_quote') == None:
                v['in_quote'] = False
            if v.get('quote_type') == None:
                v['quote_type'] = ''

        return SegmentsFV(fvs)
