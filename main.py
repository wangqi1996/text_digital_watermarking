# coding=utf-8
import math

from RSA import encrypt, pad_encrypt, decrypt, del_pad
from document_util import read_document, write_document, read_document_style
from util import count, Word


def encrypt_watermarking(file_name, mark_file_name, marks="1111000"):
    # encrypt & binary
    encrypt_mark = encrypt(code=marks)
    len_encrypt_mark = len(encrypt_mark)
    binary_mark = pad_encrypt(encrypt_mark)
    # print(binary_mark)
    binary_mark_len = int(len(binary_mark) / 8)

    # read from file && count by freq
    contents = read_document(file_name)
    word_count = count(contents)
    words = Word.get_words(word_count.keys())

    assert len(words) >= binary_mark_len, u"mark的长度超过了文本的字符数，尝试缩小mark或增长文本"
    # watermarking
    for index, word in enumerate(words[:binary_mark_len]):
        mark = binary_mark[index * 8:index * 8 + 8]
        word.set_special_style(True, mark)

    # print
    write_document(words, mark_file_name, contents=contents)

    return len_encrypt_mark


def watermarking(file_name, mark_file_name, marks="1111000"):
    # read from file && count by freq
    contents = read_document(file_name)
    word_count = count(contents)
    words = Word.get_words(word_count.keys())

    assert len(words) >= len(marks), u"mark的长度超过了文本的字符数，尝试缩小mark或增长文本"
    # watermarking
    for mark, word in zip(marks, words[:len(marks)]):
        if mark == '1':
            word.set_special_style(True, '00000001')
        else:
            word.set_special_style(False, '00000000')

    # print
    write_document(words, mark_file_name, contents=contents)

    return


def encrypt_extract(mark_file_name, len_watermark=7, marks=''):
    # read && count
    word_style = read_document_style(mark_file_name)

    contents = read_document(mark_file_name)
    word_count = count(contents)

    # marking
    watermark = ''

    for index, word in enumerate(word_count):
        if index >= math.ceil(len_watermark/8):
            break
        special_mark = word_style.get(word)
        watermark += special_mark

    # print(watermark)
    watermark = del_pad(watermark, len_watermark)
    code = decrypt(origin_code=marks, b=watermark)
    print(code)


def extract(mark_file_name, len_watermark=7):
    # read && count
    word_style = read_document_style(mark_file_name)

    contents = read_document(mark_file_name)
    word_count = count(contents)

    # marking
    watermark = ''

    for index, word in enumerate(word_count):
        if index >= len_watermark:
            break
        special = word_style.get(word)
        if special == '00000001':
            watermark += '1'
        else:
            watermark += '0'

    print(watermark)


if __name__ == '__main__':
    file_name = "data/demo.docx"
    mark_file_name = "data/demo_mark.docx"

    # 加密情况
    marks = "hello,wangqi"
    len_encrypt_mark = encrypt_watermarking(file_name, mark_file_name, marks)
    encrypt_extract(mark_file_name, len_encrypt_mark, marks)

    # 不加密情况
    marks = '1110001'
    watermarking(file_name, mark_file_name, marks=marks)
    extract(mark_file_name, len_watermark=len(marks))