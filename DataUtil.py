__author__ = 'yanw.zhao'

import re
import jieba

def get_fenci(ifile, ofile):
    inf = open(ifile, 'r', encoding='utf-8')
    onf = open(ofile, 'a', encoding='utf-8')
    all_text = re.split(u'。|；|！|？|\.|;|!|\?|，|]', inf.read().strip())
    for i in range(all_text.__len__()):
        words = jieba.lcut(all_text[i])
        for word in words:
            if not check_contain_other_words(word):
                onf.write(word + ' ')
        onf.write('\n')
    inf.close()
    onf.close()

def check_contain_other_words(check_str):
    """判断字符串是否只含有汉字数字和英文字母,含有其他字符返回Ture"""
    for ch in check_str:
        if not (is_chinese(ch) or is_number(ch) or is_alphabet(ch)):
            return True
    return False

def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if u'\u4e00' <= uchar <= u'\u9fa5':
        return True
    else:
        return False

def is_number(uchar):
    """判断一个unicode是否是数字"""
    if u'\u0030' <= uchar <= u'\u0039':
        return True
    else:
        return False

def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (u'\u0041' <= uchar <= u'\u005a') or (u'\u0061' <= uchar <= u'\u007a'):
        return True
    else:
        return False

get_fenci('./static/rawdata.txt', './static/data.txt')