import os
import pickle

import tools
from mp3tagger.pagescraper.mojim.mandarian_artist import get_names

pkl_path = tools.path('data', 'mandarian_artist.pkl')
datapath = tools.path('data')

def fetch_and_dump_mandarian_artist():
    names = []
    for name in get_names():
        names.append(name)

    if not os.path.exists(datapath):
        os.mkdir(datapath)

    with open(pkl_path, 'wb') as pkl:
        pickle.dump(list(set(names)), pkl)

if __name__ == '__main__':
    fetch_and_dump_mandarian_artist()