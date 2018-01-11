#!/usr/bin/env python3
# coding=utf-8
# author=dave.fang@outlook.com
# create=20180110

import os
import jieba
import jieba.posseg as pseg


def init_jb():
    """
    Initialize Jieba Seg Lib
    :return:
    """
    dict_path = os.path.dirname(os.path.split(os.path.realpath(__file__))[0]) + '/resources/QAattrdic.txt'
    jieba.load_userdict(dict_path)
    jieba.initialize()


def word_segment(text):
    """
    Segment words
    :param text:
    :return:
    """
    text = text.strip()
    seg_list = jieba.cut(text)
    result = " ".join(seg_list)
    return result


def pos_tag(text):
    """
    POS Tagging
    :param text:
    :return:
    """
    words = pseg.cut(text)
    return words


'''
proecss xiaohuangji corpus
'''


def xiaohuangji_textprocess(fr_path, fw_path):
    fr = open(fr_path, 'r')
    fw = open(fw_path, 'a')
    line = fr.readline()
    i = 0

    while line:
        if line[0] == 'E':
            question = fr.readline()[2:].strip()
            answer = fr.readline()[2:]
            print(question)
            print(answer)
            if len(question) < 20 and len(answer) < 30:
                i += 1
                qa_pair = question + ":::" + answer
                fw.write(qa_pair)
        line = fr.readline()

    fw.close()
    fr.close()
    print('Finished')


'''
q:::a text processing
'''


def tp2(fr_path, fw_path):
    fr = open(fr_path, 'r')
    fw = open(fw_path, 'a')
    line = fr.readline()
    while line:
        flag = 0
        words = pseg.cut(line)
        for w in words:
            print(w.word, w.flag)
            if w.flag == 'nr':
                flag = 1
        if flag == 0:
            fw.write(line)
        line = fr.readline()

    fw.close()
    fr.close()
    print('Finished')


def load_baike_attr_name(attr_dic):
    """
    Load baike attributi name
    :param attr_dic:
    :return:
    """
    fr = open(attr_dic, 'r')
    attr = []
    line = fr.readline()
    while line:
        attr.append(line.strip())
        line = fr.readline()
    fr.close()
    return attr


'''
Synonyms Analysis,return word in baike attr
word 原始词
synsdic 同义词典
attr 属性
'''


def load_synonyms_word_inattr(word, synsdic, attr):
    fr = open(synsdic, 'r')
    tar_word = ''
    line = fr.readline().strip()
    while line:
        words = line.split(" ")
        if word in words:
            for w in words:
                if w in attr:
                    tar_word = w
                    break
        if tar_word != '':
            break
        line = fr.readline()
    fr.close()
    if tar_word == '':
        tar_word = 'Empty'
    return tar_word


if __name__ == '__main__':

    tags = pos_tag("中国国家领导人是谁？")

    for tag in tags:
        print(tag)
