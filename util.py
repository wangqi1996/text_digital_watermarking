# coding=utf-8
from collections import OrderedDict


def count(content):
    sums = OrderedDict()
    for para in content:
        for word in para:
            sums.setdefault(word, 0)
            sums[word] += 1
    sums = sorted(sums.items(), key=lambda p: p[1], reverse=True)

    count_dict = OrderedDict()
    count_dict.update({
        key: value for key, value in sums
    })
    return count_dict


class Word:

    def __init__(self, word, special_style=False, mark='00000000'):
        self.word = word
        self.special_style = False
        self.mark = '00000000'

    @staticmethod
    def get_words(word_strs):
        words = []
        for word in word_strs:
            words.append(
                Word(word)
            )
        return words

    def set_special_style(self, special_style, mark='00000001'):
        self.special_style = special_style
        self.mark = mark


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


if __name__ == '__main__':
    a = hex_to_rgb("#ffffff")
    print
