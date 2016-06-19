# -*- coding: utf-8 -*-

import MeCab
import csv
import codecs
import re
import time

reply_pattern = re.compile("@.*?[ 　]")
url_pattern = re.compile('http[s]?[\S]*')


def get_new_word(text):
    mt = MeCab.Tagger("-Ochasen -d /usr/lib/mecab/dic/mecab-ipadic-neologd")

    mt.parse('')
    node = mt.parseToNode(text)

    new_word = []
    new_yomi = []

    while node:
        # print(node.surface)
        # print(node.feature)

        feature_list = node.feature.split(',')
        # print(feature_list)

        if feature_list[0] == '名詞':
            try:
                prev_word = node.surface
                # print("feature_list = %s" % feature_list)
                prev_yomi = feature_list[7]

                new_node = node.next

                next_feature_list = new_node.feature.split(',')

                if next_feature_list[0] == '名詞':
                    new_word.append(prev_word + new_node.surface)
                    new_yomi.append(prev_yomi + next_feature_list[7])

                    # print("new word = %s" % new_word)
            except IndexError as e:
                # print(e)
                pass

        node = node.next

    return new_word, new_yomi


def remove_reply_string(text):

    return reply_pattern.sub("", text)


def remove_url_string(text):

    return url_pattern.sub("", text)


def main():

    new_word = []
    new_yomi = []

    with codecs.open('data/wasara-output.csv', 'r', 'utf-8', 'ignore') as f:
        reader = csv.reader(f)
        header = next(reader)

        for row in reader:
            tweet = remove_reply_string(row[2])
            tweet = remove_url_string(tweet)
            # print("%s" % row[2])
            results, yomis = get_new_word(tweet)

            # print("result = %s, yomi = %s" % (result for result in results,
            # yomi for yomi in yomis))

            # print("result = %s, yomi = %s" % (results, yomis))

            new_word.extend(results)
            new_yomi.extend(yomis)

    print("new_word = %s" % new_word)
    print("new_yomi = %s" % new_yomi)

    with open('data/newword/wasara-newword.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        for word, yomi in zip(new_word, new_yomi):
            writer.writerow((word, yomi))


if __name__ == '__main__':
    main()
