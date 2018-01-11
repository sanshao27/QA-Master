#!/usr/bin/env python
# coding=utf-8
# author=dave.fang@outlook.com
# create=20180110

import os
import cv2
import time

from aip import AipOcr
from plugins.engine import kwquery

""" 你的 APPID AK SK """
APP_ID = '[APP_ID]'
API_KEY = '[API_KEY]'
SECRET_KEY = '[SECRET_KEY]'


def get_pic_words(file_name, client=None):
    """
    OCR 识别 / 目前使用的是百度 API
    :param file_name:
    :param client:
    :return:
    """
    file_path = './screen/{0}_half.png'.format(file_name)
    image = get_file_content(file_path)
    words = client.basicGeneral(image)
    return words['words_result']


def val_pic(file_name):
    """
    通过图片空白区域进行校验
    :param file_name:
    :return:
    """
    file_path = './screen/{0}.png'.format(file_name)
    img_raw = cv2.imread(file_path)

    w_left = int(img_raw.shape[1] * 0.1)
    w_right = int(img_raw.shape[1] * 0.1 + 20)

    w_top = int(img_raw.shape[0] * 0.15)
    w_down = int(img_raw.shape[0] * 0.15 + 20)

    img_white = img_raw[w_left:w_right, w_top:w_down]

    print(img_white.mean())

    if img_white.mean() > 240:
        return True
    else:
        return False


def main():

    while True:
        tic = time.time()

        file_name = int(time.time())
        get_pic(file_name)

        if val_pic(file_name) is False:
            continue

        cut_half(file_name, 2)
        cli = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        words = get_pic_words(file_name, cli)
        # words = [{'words': '10以下哪个是巴西过新年的独特习'}, {'words': '俗?'}, {'words': '互相揪耳朵'},
        #          {'words': '门口挂洋葱'}, {'words': '穿红色内衣裤'}]
        print(words)

        if len(words) == 0:
            continue

        i = 0
        question = ''
        for i in range(len(words) - 3):
            question += '{0}'.format(words[i]['words'])

        answers = []
        for j in range(i+1, len(words)):
            answers.append(words[j]['words'])

        print(question)
        # print(answers)

        ans = kwquery(question)
        print('================= [ Answer ] =================')
        for a in ans:
            print(a)

        toc = time.time()

        print('Time: {0}'.format(toc - tic))
        print('================= ========== =================')

        time.sleep(3)


def get_pic(file_name):
    """
    获取手机截图 / adb 方式
    :param file_name:
    :return:
    """
    os.system('adb shell screencap -p /sdcard/{0}.png'.format(file_name))
    os.system('adb pull /sdcard/{0}.png ./screen/'.format(file_name))


def cut_half(file_name, comp_type=1):
    """
    问题区域图片截图
    :param file_name:
    :param comp_type:
    :return:
    """
    file_path = './screen/{0}.png'.format(file_name)
    img_raw = cv2.imread(file_path)

    if comp_type == 1:
        # 冲顶大会
        pic_top = int(img_raw.shape[0] * 0.18)
        pic_down = int(img_raw.shape[0] * 0.60)
    else:
        # 芝士超人
        pic_top = int(img_raw.shape[0] * 0.16)
        pic_down = int(img_raw.shape[0] * 0.63)

    img_half = img_raw[pic_top:pic_down, :, :]

    cv2.imwrite('./screen/{0}_half.png'.format(file_name), img_half)


def get_file_content(file_path):
    """
    读取图片
    :param file_path:
    :return:
    """
    with open(file_path, 'rb') as fp:
        return fp.read()


if __name__ == '__main__':
    main()
