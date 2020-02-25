import logging
import os

import tools
from mp3tagger.pagescraper.youtube import YouTubeSearch
from mp3tagger.pagescraper.billboard import BB100

from tools import logger

if __name__ == '__main__':
    '''
    建立中文歌手標題資料庫
    從YouTube搜尋mandarian_artist_list中歌手的歌曲標題，
    每個歌手只抓前面10首
    '''

    path_an_artist = tools.path('data', 'mandarian_artist_list.txt')
    artists = []
    with open(path_an_artist, 'r', encoding='UTF-8') as txt:
        lines = txt.readlines()
        for line in lines:
            artists.append(line.strip())

    titles = []
    for artist in artists:
        logger.debug('Artist: {}'.format(artist))
        songs = YouTubeSearch.get_first_10_title(artist)
        if songs:
            titles.extend(songs)

    path_man_titles = tools.path('data', 'man_titles.txt')
    with open(path_man_titles, 'w', encoding='UTF-8') as txt:
        for t in titles:
            txt.write(t+'\n')
    print('')