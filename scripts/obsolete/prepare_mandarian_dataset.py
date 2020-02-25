
import os
import pickle
from typing import List

import tools
from scripts.obsolete.dump_mandarin_artists import pkl_path, fetch_and_dump_mandarian_artist
from mp3tagger.feature.features_ver0 import feature

from mp3tagger.id3youtube.labeled_artists import lart
from mp3tagger.id3youtube.labeled_title import ltit


def titles(txt: str) -> List[str]:
    with open(txt, 'r', encoding='utf-8') as titles:
        return titles.readlines()

man_dataset_path = tools.path('data', 'mandarian_dataset.pkl')

def prepare_dataset():
    if not os.path.exists(pkl_path):
        fetch_and_dump_mandarian_artist()

    # label mandarin titles using pre-labeled artist and title
    man_titles = '../data/mandarin_titles.txt'
    dataset = [feature(title.strip()) for title in titles(man_titles)]

    for vectors in dataset:
        for vector in vectors:
            if in_labeled_artist(vector['str']):
                vector.update({'label': 'artist'})
            elif in_labeled_title(vector['str']):
                vector.update({'label':'title'})


    with open(man_dataset_path, 'wb') as pkl:
        pickle.dump(dataset, pkl)

    print('')

def in_labeled_artist(name: str) -> bool:
    for vector in lart:
        if name.lower() == vector['str'].lower():
            return True

def in_labeled_title(title: str) -> bool:
    for vector in ltit:
        if title.lower() == vector['str'].lower():
            return True


def label_dataset():
    pass

if __name__ == '__main__':
    prepare_dataset()