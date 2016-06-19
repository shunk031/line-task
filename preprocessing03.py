# -*- coding: utf-8 -*-

import sys
import csv
from collections import Counter


def main():

    argvs = sys.argv
    argc = len(argvs)

    if argc == 2:
        user_name = argvs[1]
        read_file = 'data/newword/' + user_name + '-newword.csv'

        with open(read_file, 'r', encoding='utf-8') as f:

            reader = csv.reader(f)

            new_word = []
            new_yomi = []

            for row in reader:
                new_word.append(row[0])
                new_yomi.append(row[1])

            indexes = []
            counter = Counter(new_word)

            for word, cnt in counter.most_common():
                if cnt >= 3:
                    print("index= %d, %s, %d" %
                          (new_word.index(word), word, cnt))
                    indexes.append(int(new_word.index(word)))

        write_file = 'data/newword/' + user_name + '-newword-f.csv'

        with open(write_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            for index in indexes:
                # print("now index = %d" % index)
                writer.writerow((new_word[index], new_yomi[index]))


if __name__ == '__main__':
    main()
