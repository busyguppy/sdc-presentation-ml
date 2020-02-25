import pickle
import random


import os
import unicodedata

from tinytag import TinyTag

from mp3tagger.musicbrainz.musicbrainz_service import MbService
from mp3tagger.pagescraper.billboard import BB100


def artist_from_library():
    audio_ext = ["m4a", "mp3"]
    path_media = r"C:\Music"

    artists = set([])
    for root, dirs, files in os.walk(path_media):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext[1:] in audio_ext:
                path = root + "\\" + file
                tag = TinyTag.get(path)
                artists.add(tag.artist)
    return artists


man = ["蕭亞軒", "白智英", "李新潔", "張信哲", "陳勢安", "東南", "林芯儀", "鄭容和", "紀文惠", "安心亞", "蘇盈之"]


def eng_artist_from_library():
    artists = artist_from_library()

    eng_artists = []
    for name in artists:
        if name and name not in man:
            eng_artists.append(name)
    return set(eng_artists)


def man_artist_from_library():
    return set(man)


def artist_from_BB100():
    artists = BB100.artists_100()
    al = set([])
    for a in artists:
        al.add(a.title)
    return al


def artist_from_txt():
    path_a_list = "mandarian_artists.txt"
    artists = []
    with open(path_a_list, "r", encoding="UTF-8") as txt:
        for line in txt:
            artists.append(line.strip())
    return set(artists)


temp_artist = "continue_query.pkl"
temp_info = "query_data.pkl"


def fetch_artistInfo_in_a_recoverable_manner(artists_pkl: str, artist_infos_pkl: str):
    titles = []
    artist_titles = []
    if not os.path.exists(temp_artist):
        with open(artists_pkl, "rb") as pkl:
            artist_titles = pickle.load(pkl)
    else:
        with open(temp_artist, "rb") as pkl:
            artist_titles = pickle.load(pkl)

    a_infos = []
    if os.path.exists(temp_info):
        with open(temp_info, "rb") as pkl:
            a_infos = pickle.load(pkl)

    while len(artist_titles) > 0:
        title = artist_titles.pop()
        if not title:
            continue
        try:
            artist_info = MbService.query_artist(title)
            if artist_info is not None:
                a_infos.append(artist_info)
        except:
            artist_titles.append(title)

        with open(temp_artist, "wb") as pkl:
            pickle.dump(artist_titles, pkl)
        with open(temp_info, "wb") as pkl:
            pickle.dump(a_infos, pkl)
        show_how_many_artists_remains()

    with open(artist_infos_pkl, "wb") as pkl:
        pickle.dump(a_infos, pkl)

    if os.path.exists(temp_artist):
        os.remove(temp_artist)
    if os.path.exists(temp_info):
        os.remove(temp_info)


def show_how_many_artists_remains():
    artist_titles = []
    if not os.path.exists(temp_artist):
        return
    with open(temp_artist, "rb") as pkl:
        artist_titles = pickle.load(pkl)
    print("Still {} artists to go!".format(len(artist_titles)))


if __name__ == "__main__":
    # 1. 準備歌手清單
    if (
        not os.path.exists("eng_artist.pkl")
        or not os.path.exists("man_artist.pkl")
        or not os.path.exists("artist.pkl")
    ):
        eng_artists = eng_artist_from_library().union(artist_from_BB100())
        man_artists = man_artist_from_library().union(artist_from_txt())
        artists = eng_artists.union(man_artists)

        with open("eng_artist.pkl", "wb") as pkl:
            pickle.dump(list(eng_artists), pkl)
        with open("man_artist.pkl", "wb") as pkl:
            pickle.dump(list(man_artists), pkl)
        with open("artist.pkl", "wb") as pkl:
            pickle.dump(list(artists), pkl)

    # Query Artists Info from MusicBrainz
    # 2.
    if not os.path.exists("eng_artist_infos.pkl"):
        fetch_artistInfo_in_a_recoverable_manner(
            "eng_artist.pkl", "eng_artist_infos.pkl"
        )
    if not os.path.exists("man_artist_infos.pkl"):
        fetch_artistInfo_in_a_recoverable_manner(
            "man_artist.pkl", "man_artist_infos.pkl"
        )
    if not os.path.exists("artist_infos.pkl"):
        eng = []
        man = []
        with open("eng_artist_infos.pkl", "rb") as pkl:
            eng = pickle.load(pkl)
        with open("man_artist_infos.pkl", "rb") as pkl:
            man = pickle.load(pkl)
        with open("artist_infos.pkl", "wb") as pkl:
            eng.extend(man)
            pickle.dump(eng, pkl)
        with open("artists.txt", "w", encoding="UTF-8") as pkl:
            for a in eng:
                pkl.write(a.name + "\n")

    # 檢查資料
    eng_artist = []
    with open("eng_artist.pkl", "rb") as pkl:
        eng_artists = pickle.load(pkl)
    eng_artist_infos = []
    with open("eng_artist_infos.pkl", "rb") as pkl:
        eng_artist_infos = pickle.load(pkl)
    man_artists = []
    with open("man_artist.pkl", "rb") as pkl:
        man_artists = pickle.load(pkl)
    man_artist_infos = []
    with open("man_artist_infos.pkl", "rb") as pkl:
        man_artist_infos = pickle.load(pkl)
    all_infos = []
    with open("artist_infos.pkl", "rb") as pkl:
        all_infos = pickle.load(pkl)
    print("準備英文歌手：{}筆".format(len(eng_artists)))
    print("取得英文歌手資料：{}筆".format(len(eng_artist_infos)))
    print("準備中文歌手：{}筆".format(len(man_artists)))
    print("取得中文歌手資料：{}筆".format(len(man_artist_infos)))
    print("總共取得資料：{}筆".format(len(all_infos)))

    t = 1
