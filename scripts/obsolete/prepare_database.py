import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Column, BLOB, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tinytag import TinyTag

Base = declarative_base()

class Audio(Base):
    __tablename__ = 'audio'

    def __init__(self, path='', artist='', album='', title=''):
        self.path = path
        self.artist = artist
        self.album = album
        self.title = title

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String)
    artist = Column(String)
    album = Column(String)
    title = Column(String)
    filename = Column(String)


class DataAccessLayer():
    def __init__(self):
        self.engine = create_engine('sqlite:///dataset.db', echo=False)
        Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

def prepare_database():
    if os.path.exists('dataset.db'):
        os.remove('dataset.db')
    dal = DataAccessLayer()
    session = dal.session

    media_path = r'c:\music'
    audio_ext = ['.mp3', '.m4a']

    for root, dirs, files in os.walk(media_path):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext in audio_ext:
                audio = Audio()
                audio.path = root + '\\' + file
                tag = TinyTag.get(audio.path)
                audio.artist = tag.artist
                audio.album = tag.album
                audio.title = tag.title
                audio.filename = '{} - {} - {}'.format(audio.artist,
                                                       audio.album,
                                                       audio.title)

                if audio.album == 'YouTube':
                    continue
                session.add(audio)
        session.commit()




