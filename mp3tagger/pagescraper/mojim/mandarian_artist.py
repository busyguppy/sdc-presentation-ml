from typing import Generator

import parsel
import requests


def gen_urls() -> Generator[str, None, None]:
    '''
    https://mojim.com/twzlha_01.htm => 華語男生(01~07)
    https://mojim.com/twzlhb_01.htm => 華語女生(01~07)
    https://mojim.com/twzlhc_01.htm => 華語團體(01~33)
    '''

    for gender in ['a', 'b']:
        for page in range(1, 8):
            yield "https://mojim.com/twzlh{}_{:02d}.htm".format(gender, page)
    for page in range(1, 34):
        yield "https://mojim.com/twzlhc_{:02d}.htm".format(page)


def get_names() -> Generator[str, None, None]:
    for url in gen_urls():
        html = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text
        selector = parsel.Selector(html)
        titles = selector.xpath("//ul[@class='s_listA']/li/a/@title").getall()
        for t in titles:
            name, _ = t.strip().rsplit(' ', 1)
            yield name