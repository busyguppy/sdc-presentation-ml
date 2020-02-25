
class Artist:
    id = None
    type = None
    name = None
    gender = None
    country = None
    release_groups = None
    releases = None

    def __init__(self):
        pass

# from sqlalchemy import Column, String
#
# from mp3tagger.musicbrainz import Base
#
# class Artist:
#     __tablename__ = 'artist'
#
#     id = Column(String(40), primary_key=True)
#     type = Column(String(10))
#     name = Column(String(40))
#     gender = Column(String(10))
#     country = Column(String(20))
#     # alias-list = []
#     # life-span 1995-03-11
#