import time
from urllib import request
from datetime import datetime as dt

import csv
import sys
import pandas as pd
from bs4 import BeautifulSoup


class TwilogParser:

    def __init__(self):
        self.account = None

    def set_account(self, target_account):
        self.account = target_account

    def get_page_df(self, num):
        url = self.make_twilog_url(num)
        soup = self.make_soup(url)
        return self.soup_to_df(soup)

    def make_twilog_url(self, num):
        base_url = "http://twilog.org/%s/" % self.account
        if num <= 1:
            return base_url
        else:
            return base_url + "%d" % num

    def make_soup(self, url):
        with request.urlopen(url) as response:
            html = response.read()
        return BeautifulSoup(html, "lxml")

    def soup_to_df(self, soup):
        daily_titles = soup.findAll('h3', class_='title01')
        daily_dfs = [self._daily_titles_to_df(d) for d in daily_titles]
        return pd.concat(daily_dfs)  # 各日付のDataFrameが入ったリストを結合する

    def _get_tweet_texts(self, tweets):
        return [t.find(class_='tl-text').text for t in tweets]

    def _daily_titles_to_df(self, daily_title):
        # date = self._to_date(daily_title.find('a'))
        tweets = daily_title.findNext('section').findAll(class_='tl-tweet')
        # return self._tweets_to_df(tweets, date)
        return self._tweets_to_df(tweets)

    def _tweets_to_df(self, tweets):
        dailydata = {
            'text': self._get_tweet_texts(tweets)
        }
        df = pd.DataFrame(dailydata)

        return df


def main():

    argvs = sys.argv
    argc = len(argvs)

    if argc == 2:

        input_file = 'data/follower_list/' + argvs[1] + '.csv'

        with open(input_file, 'r') as f:
            reader = csv.reader(f)
            userlists = [row for row in reader]

            userlist = [flatten for inner in userlists for flatten in inner]

            for username in userlist:
                parser = TwilogParser()
                parser.set_account(username)

                try:
                    for i in range(100):
                        if i == 0:
                            df = parser.get_page_df(i + 1)
                        else:
                            df = pd.concat([df, parser.get_page_df(i + 1)])

                        print("%s, now page %d" % (username, i + 1))
                        time.sleep(1)
                except ValueError as e:
                    print(e)

                output_file = 'data/' + username + '-output.csv'

                try:
                    df.to_csv(output_file, index=False)
                except UnboundLocalError as e:
                    print(e)
    else:
        print("You should give input file name")


if __name__ == '__main__':
    main()
