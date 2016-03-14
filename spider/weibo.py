# -*- coding: utf8 -*-
u'''
@summary:
@author: Administrator
@date: 2016年3月14日
'''
import base64
import binascii
import simplejson
import re
import traceback
import urllib

import requests
import rsa


class Weibo(object):
    def __init__(self, username, passwd):
        self.sess = requests.Session()
        self.username = username
        self.passwd = passwd

    def _get_user(self, username):
        username = urllib.quote(username)
        return base64.encodestring(username)[:-1]

    def _get_passwd(self, passwd, pubkey, servertime, nonce):
        key = rsa.PublicKey(int(pubkey, 16), int('10001', 16))
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(passwd)
        passwd = rsa.encrypt(message, key)
        return binascii.b2a_hex(passwd)

    def _prelogin(self):
        username = self._get_user(self.username)
        prelogin_url = (r'http://login.sina.com.cn/sso/prelogin.php?'
                        'entry=sso&callback=sinaSSOController.preloginCallBack'
                        '&su=%s&rsakt=mod&client=ssologin.js(v1.4.18)' % username)

        data = self.sess.get(prelogin_url)
        regex = re.compile('\((.*)\)')
        try:
            json_data = regex.search(data.content).group(1)
            data = simplejson.loads(json_data)

            return str(data['servertime']), data['nonce'], data['pubkey'], data['rsakv']
        except Exception:
            traceback.print_exc()

    def login(self):
        login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'

        try:
            servertime, nonce, pubkey, rsakv = self._prelogin()
            postdata = {
                'entry': 'weibo',
                'gateway': '1',
                'from': '',
                'savestate': '7',
                'userticket': '1',
                'ssosimplelogin': '1',
                'vsnf': '1',
                'vsnval': '',
                'su': self._get_user(self.username),
                'service': 'miniblog',
                'servertime': servertime,
                'nonce': nonce,
                'pwencode': 'rsa2',
                'sp': self._get_passwd(self.passwd, pubkey, servertime, nonce),
                'encoding': 'UTF-8',
                'prelt': '115',
                'rsakv' : rsakv,
                'url': ('http://weibo.com/ajaxlogin.php?framelogin=1&amp;'
                        'callback=parent.sinaSSOController.feedBackUrlCallBack'),
                'returntype': 'META'
            }
            text = self.sess.post(login_url, data=postdata).content
#             print "text", text
            ajax_url_regex = re.compile('location\.replace\(\'(.*)\'\)')
            matches = ajax_url_regex.search(text)

#             print "matches", matches
            if matches is not None:
                ajax_url = matches.group(1)
                content = self.sess.get(ajax_url).content
            else:
                return False, "Can't find redirect url! Check the account info!"
#             print 'content:', content

            regex = re.compile('\((.*)\)')
            json_data = simplejson.loads(regex.search(content).group(1))
#             print json_data

            result = json_data['result'] == True
            if result is False and 'reason' in json_data:
                return result, json_data['reason']
            return result, ""
        except Exception:
            traceback.print_exc()
            return False, ""



