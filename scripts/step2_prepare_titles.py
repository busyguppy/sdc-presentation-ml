import copy
import datetime
import os
import pickle
import random

import mp3tagger.tools
from mp3tagger.tools import logger
from mp3tagger.classes.titleinfo import TitleInfo
from mp3tagger.musicbrainz import Artist
from mp3tagger.musicbrainz.musicbrainz_service import MbService
from mp3tagger.pagescraper.youtube import YouTubeSearch


def show_artistInfo():
    a_infos = []
    with open('artist_infos.pkl', 'rb') as pkl:
        a_infos = pickle.load(pkl)
    print('總共蒐集了{}個歌手資料!'.format(len(a_infos)))
    return a_infos

def all_track_titles(artist: Artist):
    track_titles = set([])
    for group in artist.release_groups:
        rel = None
        for release in artist.releases:
            if group.title == release.title:
                if rel == None:
                    rel = release
                else:
                    d1 = None
                    d2 = None
                    try:
                        d1 = datetime.datetime.strptime(rel.date, '%Y-%m-%d')
                        d2 = datetime.datetime.strptime(release.date, '%Y-%m-%d')
                        rel = release if d2 <= d1 else rel  # 找出同Release Group最早Release
                        rel = release if d2 <= d1 else rel  # 找出同Release Group最早Release
                    except ValueError:
                        pass
                    if d1 is None and d2 is not None:
                        rel = release
                        continue

        if rel is not None:
            for medium in rel.medium_list:
                for track in medium.tracklist:
                    track_titles.add(track.recording.title)

    return list(track_titles)


def random_10_tracks(artist: Artist):
    tracks = all_track_titles(artist)
    return random.sample(tracks, min(len(tracks), 10))


def fetch_titleInfo_in_a_recoverable_manner(artist_info_path: str, title_info_path):
    # 326個歌手資料
    a_infos = []
    with open(artist_info_path, 'rb') as pkl:
        a_infos = pickle.load(pkl)


    title_infos = set([])
    for a in a_infos:
        for t_title in random_10_tracks(a):
            title_info = TitleInfo()
            title_info.artist = a.name
            title_info.song_title = t_title
            title_infos.add(title_info)

    old = 'old_titleInfo.pkl'
    new = 'new_titleInfo.pkl'
    title_infos = list(title_infos)
    new_title_infos = []

    if os.path.exists(old):
        with open(old, 'rb') as pkl:
            title_infos = pickle.load(pkl)
    if os.path.exists(new):
        with open(new, 'rb') as pkl:
            new_title_infos = pickle.load(pkl)


    i = 0
    while len(title_infos) > 0:
        t_info = title_infos.pop()
        logger.debug('{} - {}'.format(t_info.artist, t_info.song_title))
        titles = YouTubeSearch.get_first_10_title(t_info.artist, t_info.song_title)
        t = 100
        if len(titles) < 2:
            continue
        titles = random.sample(titles, min(len(titles), 2))

        old_info = copy.deepcopy(t_info)
        t_info.title = titles[0]
        old_info.title = titles[1]
        new_title_infos.append(t_info)
        new_title_infos.append(old_info)
        i += 1
        if i == 50:
            with open(old, 'wb') as pkl:
                pickle.dump(title_infos, pkl)
            with open(new, 'wb') as pkl:
                pickle.dump(new_title_infos, pkl)
            logger.debug('暫存資料中...')
            i = 0

    with open(title_info_path, 'wb') as pkl:
        pickle.dump(new_title_infos, pkl)

    if os.path.exists('old_titleInfo.pkl'):
        os.remove('old_titleInfo.pkl')
    if os.path.exists('new_titleInfo.pkl'):
        os.remove('new_titleInfo.pkl')

if __name__ == '__main__':

    '''
    1.  用eng_artist_infos, man_artist_infos上YouTube爬影片標題，
        收集後存放在eng_title_infos.pkl, man_title_infos.pkl
    '''
    if not os.path.exists('eng_title_infos.pkl'):
        fetch_titleInfo_in_a_recoverable_manner('eng_artist_infos.pkl', 'eng_title_infos.pkl')
    if not os.path.exists('man_title_infos.pkl'):
        fetch_titleInfo_in_a_recoverable_manner('man_artist_infos.pkl', 'man_title_infos.pkl')
    if not os.path.exists('title_infos.pkl'):
        eng = []
        with open('eng_title_infos.pkl', 'rb') as pkl:
            eng = pickle.load(pkl)
        man = []
        with open('man_title_infos.pkl', 'rb') as pkl:
            man = pickle.load(pkl)
        with open('title_infos.pkl', 'wb') as pkl:
            eng.extend(man)
            pickle.dump(eng, pkl)


    # 3. 總共收集5092筆有歌手、歌曲名稱標記資料
    title_infos = []
    with open('title_infos.pkl', 'rb') as pkl:
        title_infos = pickle.load(pkl)


    # 4. 輸出歌曲資料供labeler使用
    title_txt = mp3tagger.data_file('titles.txt')
    with open(title_txt, 'w', encoding='UTF-8') as txt:
        for info in title_infos:
            txt.write(info.title + '\n')
