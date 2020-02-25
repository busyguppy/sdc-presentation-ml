import logging
import os
from typing import List

import requests
from bs4 import BeautifulSoup

import tools
from mp3tagger.pagescraper.billboard import Artist

from tools import logger

class BB100:
    @staticmethod
    def artists_100() -> List[Artist]:
        url = 'https://www.billboard.com/charts/artist-100'
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')

        if logger.level == logging.DEBUG:
            temp_dir = tools.path('temp')
            bb_temp = tools.path('temp', 'bb100_artists.html')
            if not os.path.exists(temp_dir):
                os.mkdir(temp_dir)
            with open(bb_temp, 'w', encoding='UTF-8') as h:
                h.write(response.text)

        artists = []

        chart_list_items = soup.find_all('div', {'class': 'chart-list-item'})
        for item in chart_list_items:
            a = Artist()
            a.title  = item.find_all('span', {'class': 'chart-list-item__title-text'})[0].text.strip()
            cell = item.find_all('div', {'class': 'chart-list-item__ministats-cell'})
            a.last_week_position = cell[0].next.strip()
            a.peak_postion = cell[1].next.strip()
            a.on_chart_weeks = cell[2].next.strip()
            artists.append(a)

        return artists



if __name__ == '__main__':

    for a in BB100.artists_100():
        print(a.title)
