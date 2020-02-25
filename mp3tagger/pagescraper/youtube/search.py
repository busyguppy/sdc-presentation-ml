import logging
import os
import re
import urllib

from bs4 import BeautifulSoup
from lxml import html
import requests
import tools

from tools import logger

class YouTubeSearch:

    @staticmethod
    def get_first_10_title(artist: str, track_title: str):
        alower = artist.lower()
        ttlower = track_title.lower()
        s_str = YouTubeSearch.format_str(artist, track_title)
        url = 'https://www.youtube.com/results?search_query={}&pbj=1'.format(s_str)
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

        tree = html.fromstring(response.text)
        titles = []
        for content in tree.xpath('//div[@class="yt-lockup-content"]/h3/a'):
            href = content.xpath('attribute::href')[0]
            title = content.xpath('attribute::title')[0]
            tlower = title.lower()
            if any([k in href for k in['list=', 'channel', 'googleadservices']])\
                    or alower not in tlower\
                    or ttlower not in tlower:
                continue
            else:
                titles.append(title)


        # TODO: 尋找ajax讀取更多資料的方法
        # # span class多了個空白，以後可能被改掉
        # data_href = tree.xpath('//span[@class=" yt-uix-button-subscription-container"]//button/attribute::data-href')
        # # No more search results
        # if len(data_href) == 0:
        #     pass
        # else:   # More search results to be loaded
        #     ctoken_text = urllib.parse.unquote(data_href[0])
        #     pattern = re.compile('continue_action=([^%]*)')
        #     ctoken = re.findall(pattern, ctoken_text)[0]
        #
        #     # xpath一直抓不到@@
        #     # itct_link = tree.xpath('a[@class="yt-uix-button vve-check yt-uix-sessionlink yt-uix-button-default yt-uix-button-size-default"]')
        #     soup = BeautifulSoup(response.text, 'html.parser')
        #     itct_tags = soup.findAll('a', {'class': 'yt-uix-button vve-check yt-uix-sessionlink yt-uix-button-default yt-uix-button-size-default'})
        #     itct_tags.pop()  # 最後一個是下一頁連結，跟第一個一樣
        #     pattern = re.compile('itct=(.*)')
        #     for tag in itct_tags:
        #         data_sessionlink = tag['data-sessionlink']
        #         itct = re.findall(pattern, data_sessionlink)[0]
        #         ajax_pat = 'https://www.youtube.com/results?search_query={keyword}&pbj=1&ctoken={ctoken}%3D&itct={itct}'
        #         ajax_url = ajax_pat.format(keyword=s_str, ctoken=ctoken, itct=itct)
        #         response = requests.get(ajax_url, headers={'User-Agent': 'Mozilla/5.0'})
        #         print('')

        return titles if len(titles) <= 10 else titles[0:10]

    @staticmethod
    def format_str(*args):
        temp = ''
        for s in args:
            temp += '%22' + s.replace(' ','+') + '%22'+'+'
        return temp[:-1]


if __name__ == '__main__':
    titles = YouTubeSearch.get_first_10_title('Sasha Sloan', 'dancing with your ghost')
    print('')

    # urlencoded = 'https://www.youtube.com/results?search_query=sasha+sloan&pbj=1&ctoken=%253D&itct=CF4QybcCIhMIk9jI9b6l5wIVhDcqCh1tVQMi'
    # txt = urllib.parse.unquote(urlencoded)
    # print(txt)
