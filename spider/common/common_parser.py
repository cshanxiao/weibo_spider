# -*- coding: utf8 -*-

import simplejson
import re

from bs4 import BeautifulSoup

from spider.log import logging as log

class CommonParser(object):

    def is_visitor(self, html):
        '''
        :param html:
        :return: Ture if this account is in visitor status
        '''
        soup = BeautifulSoup(html)
        if 'Sina Visitor System' in soup.find('title').text:
            return True
        return False

    def parse_is_enterprise(self, html):
        '''
        :param html:  Ture if this page's owner is an enterprise user
        :return:
        '''
        soup = BeautifulSoup(html)
        scripts = soup.find_all('script')
        frame = None  # frame that contains avatar, background ...

        for scr in scripts:
            if ur'class=\"photo\"' in scr.text:
                frame = scr
                break

        if frame is None:
            return None  # dirty html

        html = self.covert_script_to_hmtl(frame)
        soup = BeautifulSoup(html)

        if soup.find('em', 'W_icon icon_pf_approve_co') is not None:
            return True
        else:
            return False


    def is_exceptional(self, html):
        soup = BeautifulSoup(html)
        if u'您当前使用的账号存在异常，请完成以下操作解除异常状态' in soup.text:
            return True
        return False

    def is_frozen(self, html):
        soup = BeautifulSoup(html)
        try:
            if u'微博帐号解冻' in soup.find('title').text:
                return True
            return False
        except:
            return False

    def parse_pid(self, html):
        """
        :param html:
        :return: pid if exception occurs return None
        """
        soup = BeautifulSoup(html)
        script = soup.find('script', text=re.compile("\$CONFIG\[\'page_id\'\]"))
        try:
            script = script.text
            attributes = script.split(';')
            pid = ''
            for attr in attributes:
                if 'page_id' in attr:
                    pid = attr.split('=')[1][1:-1]
                    pid = str(pid)  # convert unicode to string
                    return pid
        except Exception as e:
            log.error(e.message)
            return None

    def parse_uid(self, html):
        soup = BeautifulSoup(html)
        script = soup.find('script', text=re.compile("\$CONFIG\[\'page_id\'\]"))

        try:
            script = script.text
            attributes = script.split(';')
            uid = ''
            for attr in attributes:
                if 'uid' in attr:
                    uid = attr.split('=')[1][1:-1]
                    uid = str(uid)  # convert unicode to string
                    return uid
            return -1  # no uid
        except Exception as e:
            log.error(e.message)
            return None

    def covert_script_to_hmtl(self, script):
        """
        :param script: a bs4 tag object
        :return: html if failed return None
        """
        script = script.text
        try:
            json_text = script[8:-1]
            return simplejson.loads(json_text)['html']
        except Exception as e:
            log.error(e.message)
            return None

    def get_max_page_num(self, links):
        '''
        :param links: a list of links, which contain page numbers
        :return: max page number
        '''
        max_pnum = 0
        for link in links:
            pnum = link.text
            if not pnum.isdigit():
                continue
            pnum = int(pnum)
            if pnum > max_pnum:
                max_pnum = pnum
        return max_pnum

    def parse_is_taobao(self, html):
        '''
        :param html:
        :return: '1' is taobao, '0' is not
        '''
        if html is None:
            return None
        keyword = 'W_icon icon_taobao'
        soup = BeautifulSoup(html)
        scripts = soup.find_all('script')
        script = None
        for scr in scripts:
            if u'PCD_person_info' in scr.text:
                script = scr
                break
        if script is None:
            return None  # dirty html

        html = self.covert_script_to_hmtl(script)
        soup = BeautifulSoup(html)
        person_info = soup.find('div', 'PCD_person_info')
        taobao = person_info.find('em', keyword)

        if taobao is not None:
            return '1'
        return '0'

