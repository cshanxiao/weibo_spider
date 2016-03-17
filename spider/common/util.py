# -*- coding: utf8 -*-
u'''
@summary:
@author: Administrator
@date: 2016年03月15日
'''

def strip_blanks(text):
    text = text.replace('\r', '').replace('\n', '').replace('\t', '')
    text = text.strip(' ')
    return text

def strip_parentheses(text):
    """
    @summary: strip '(' and ')'
    """
    return text.strip('(').strip(')')


