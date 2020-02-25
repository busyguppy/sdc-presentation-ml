import csv
import logging
import pickle
from typing import List

from mp3tagger.classes.feature_tool import FeatureTool
from mp3tagger.classes.segments_feature_vector import SegmentsFV
from mp3tagger.classes.titleinfo import TitleInfo
from mp3tagger.tools import logger, data_file


def load_titleInfos(path='title_infos.pkl'):
    title_infos = []
    with open(path, 'rb') as pkl:
        title_infos = pickle.load(pkl)
    return title_infos

def extract_features(title_infos: List[TitleInfo]):
    ft = FeatureTool()
    dataset = []
    for info in title_infos:
        info.feature_vectors = ft.feature_vectors(info.title)

        for fv in info.feature_vectors:
            if fv['str'].lower() == info.artist.lower():
                fv['label'] = 'a'
            elif fv['str'].lower() == info.song_title.lower():
                fv['label'] = 't'
            else:
                fv['label'] = 'x'

        artist_found = False
        title_found = False
        for fv in info.feature_vectors:
            if fv['label'] == 'a':
                artist_found = True
            if fv['label'] == 't':
                title_found = True

        if artist_found and title_found:
            dataset.append(info)
    return dataset

if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)

    # 讀取2_prepare_titles準備好的資料, title_infos.pkl
    # 總共5092個標題資料
    title_infos = load_titleInfos()

    # 3107個標題比對到到歌手、歌曲
    dataset = extract_features(title_infos)


    t = 1

    # pickle dataset
    path_dataset = data_file('dataset.pkl')
    with open(path_dataset, 'wb') as pkl:
        fvs = []
        for info in dataset:
            fvs.append(info.feature_vectors)
        pickle.dump(fvs, pkl)

    # 輸出csv
    # dataset_path = tools.data_file('dataset.csv')
    # with open(dataset_path, 'w', newline='\n', encoding='utf-8') as f:
    #     cw = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     cw.writerow(['tag', 'str', 'label', 'i_seg', 'str_len_left', 'seg_len', 'left_lo_seg_cnt',
    #                  'title_len', 'right_seg_cnt', 'right_seg_length', 'right_lo_seg_cnt',
    #                  'i_slot_between_dash', 'in_quote', 'quote_type'])
    #     for info in dataset:
    #         for fv in info.feature_vectors:
    #             cw.writerow([fv['tag'], fv['str'], fv['label'], fv['i_seg'], fv['str_len_left'],
    #                         fv['seg_len'], fv['left_lo_seg_cnt'], fv['title_len'],
    #                         fv['right_seg_cnt'], fv['right_seg_length'], fv['right_lo_seg_cnt'],
    #                         fv['i_slot_between_dash'], fv['in_quote'], fv['quote_type']])

    t = 1

