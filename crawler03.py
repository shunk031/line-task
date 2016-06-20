# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import csv

user_names = []


def get_user_name(url):

    target_url = url

    try:
        html = urlopen(target_url)
    except HTTPError as e:
        print(e)

    soup = BeautifulSoup(html.read(), "lxml")
    spanTags = soup.findAll("span", {"class": "author-username"})

    for spanTag in spanTags:
        aTag = spanTag.find("a")
        user_name = aTag.get_text().replace("@", "")
        user_names.append(user_name)


def main():
    # url = 'http://meyou.jp/ranking/follower_journalist'
    url = 'http://meyou.jp/ranking/follower_artist'
    url = 'http://meyou.jp/ranking/follower_creator'
    url = 'http://meyou.jp/ranking/follower_profession'
    url = 'http://meyou.jp/ranking/follower_talent'
    url = 'http://meyou.jp/ranking/follower_ceo'
    url = 'http://meyou.jp/ranking/follower_developer'
    url = 'http://meyou.jp/ranking/follower_freelance'

    filename = 'data/follower_list/' + 'follower_freelance' + '.csv'

    target_url = url

    for i in range(0, 5000, 50):
        if i == 0:
            get_user_name(target_url)
        else:
            get_user_name(target_url + "/%d" % i)

    with open(filename, "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(user_names)


if __name__ == '__main__':
    main()
