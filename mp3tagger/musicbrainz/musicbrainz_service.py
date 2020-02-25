import logging
import operator
import time
from datetime import datetime
import random
from typing import List
from mp3tagger.musicbrainz import Artist, Release, Recording, Medium, ReleaseGroup

from mp3tagger.bootstrap.musicbrainz_useragent import *
from mp3tagger.musicbrainz.entities.track import Track

from tools import logger

class MbService:

    @staticmethod
    def query_artist(name: str) -> Artist:
        result = mb.search_artists(artist=name)

        for artist in result['artist-list']:
            if artist['name'].lower() == name.lower():
                logger.debug('Artist: {}'.format(artist['name']))
                a = Artist()
                MbService.__assign_artist_attr(a, artist)


                a.release_groups, a.releases = MbService.__get_release_info(a.id)
                # a.releases = MbService.__get_releases(a.id)

                for rel in a.releases:
                    rel.medium_list = MbService.__get_medium_list(rel.id)
                    # for medium in medium_list:

                # 找到第一個完全匹配的就傳回
                return a
        return None

    @staticmethod
    def __get_release_info(artist_id: str):
        inc = ['release-groups', 'releases']
        result = mb.get_artist_by_id(artist_id, includes=inc, release_type=["album", 'ep'])

        groups =[]
        for release_group in result['artist']['release-group-list']:
            g = ReleaseGroup()
            g.id = release_group.get('id', '')
            g.type = release_group.get('type', '')
            g.title = release_group.get('title', '')
            g.first_release_date = release_group.get('first-release-date', '')
            g.primary_type = release_group.get('primary-type', '')
            groups.append(g)

        releases = []
        for rel in result["artist"]["release-list"]:
            r = Release()
            r.id = rel.get('id', '')
            r.title = rel.get('title', '')
            r.status = rel.get('status', '')
            r.quality = rel.get('quality', '')
            txt_pepr = rel.get('text-representation', '')
            if txt_pepr:
                r.language = txt_pepr.get('language', '')
            r.date = rel.get('date', '')
            r.country = rel.get('country', '')
            releases.append(r)
        releases = sorted(releases, key=operator.attrgetter('date'))
        return (groups, releases)


    @staticmethod
    def __assign_artist_attr(artist: Artist, data: dict):
        artist.id = data.get('id', '')
        artist.name = data.get('name', '')
        artist.type = data.get('type', '')
        artist.gender = data.get('gender', '')
        artist.country = data.get('country', '')

    @staticmethod
    def __get_releases(rid: str) -> List[Release]:
        inc = ['releases']
        result = mb.get_artist_by_id(rid, includes=inc, release_type=["album", 'ep'])

        releases = []
        for rel in result["artist"]["release-list"]:
            r = Release()
            r.id = rel.get('id', '')
            r.title = rel.get('title', '')
            r.status = rel.get('status', '')
            r.quality = rel['quality']
            txt_repr = rel.get('text-representation', '')
            if txt_repr:
                r.language = txt_repr.get('language', '')
            r.date = rel['date']
            r.country = rel['country']
            releases.append(r)

        return sorted(releases, key=operator.attrgetter('date'))

    @staticmethod
    def __get_medium_list(id: str):
        result = mb.get_release_by_id(id, includes=['recordings'])

        medium_list = []
        for medium in result['release']['medium-list']:
            m = Medium()
            m.position = medium.get('position', '')
            m.format = medium.get('format', '')

            track_list = []
            for track in medium['track-list']:
                t = Track()
                t.id = track.get('id', '')
                t.position = track.get('position', '')
                t.number = track.get('number', '')
                t.length = track.get('length', '')

                r = Recording()
                r.id = track['recording']['id']
                r.title = track['recording']['title']
                r.length = track['recording'].get('length', '')
                t.recording = r

                track_list.append(t)
                m.tracklist = track_list

            medium_list.append(m)

        return medium_list

    @staticmethod
    def all_track_title(artist: str):
        artist = MbService.query_artist(artist)


        track_titles = set([])
        for group in artist.release_groups:
            rel = None
            for release in artist.releases:
                if group.title == release.title:
                    if rel == None: rel = release
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

    @staticmethod
    def random_10_tracks(artist: str):
        titles = MbService.all_track_title(artist)
        return random.sample(titles, k=min(len(titles), 10))

if __name__ == '__main__':
    t1 = time.time()
    # Sasha Sloan
    # 98c09f94-10b5-426c-b27a-44345bb54528
    # artist = MbService.query_artist('Sasha Sloan')
    # artists = MbService.query_artist('張信哲')
    # track_titles = MbService.all_track_title('Sasha Sloan')
    random_10 = MbService.random_10_tracks('Sasha Sloan')

    logger.debug('\n總執行時間：{:.2f} 秒'.format(time.time() - t1))


