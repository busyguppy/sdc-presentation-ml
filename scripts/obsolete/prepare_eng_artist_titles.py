import logging
import os

import tools
from mp3tagger.pagescraper.youtube import YouTubeSearch
from mp3tagger.pagescraper.billboard import BB100

from tools import logger

if __name__ == '__main__':
    '''
    建立英文歌手標題資料庫
    從YouTube搜尋BillBoard 100 hot artist歌曲標題，
    每個歌手只抓前面10首
    '''

    # 爬Billboard 100大熱門歌手
    # https://www.billboard.com/charts/artist-100
    artists = BB100.artists_100()

    # MusicBrainz上查每個歌手最新10首歌


    titles = []
    for artist in artists:
        logger.debug('Artist: {}'.format(artist.title))
        songs = YouTubeSearch.get_first_10_title(artist.title)
        if songs:
            titles.extend(songs)

    datapath = tools.path('data')
    path_en_title = tools.path('data', 'eng_titles.txt')
    if not os.path.exists(datapath):
        os.mkdir(datapath)
    with open(path_en_title, 'w', encoding='utf-8') as txt:
        for t in titles:
            txt.write(t+'\n')

    print('')