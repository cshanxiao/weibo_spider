# -*- coding: utf8 -*-
u'''
@summary:
@author: Administrator
@date: 2016年3月14日
'''
import redis
import time
from datetime import datetime

from spider.common.followee_parser import FolloweeParser
from spider.log import log
from spider.weibo import Weibo


class VipSpider(Weibo):
    def __init__(self):
        Weibo.__init__(self)
        self.parser = FolloweeParser()

    def ban_account(self):
        url = 'http://sass.weibo.com/unfreeze'
        html = self.sess.get(url)
        is_exceptional = self.parser.is_exceptional(html)
        is_frozen = self.parser.is_frozen(html)
        if is_exceptional is False and is_frozen is False:
            return

    def get_followees(self, pid):
        url = 'http://www.weibo.com/p/' + pid + '/follow?from=page_' + pid[:6] + '&wvr=6&mod=headfollow#place'
        while True:
            html = self.sess.get(url)
            uid = self.parser.parse_uid(html)
            if uid == -1:
                continue
            elif self.parser.is_visitor(html) is True:
                self.reset_account()
                continue

            fee_page_num = self.parse_followee_page_num(html)
            if fee_page_num is not None:
                break
            else:
                log.warning('Cannot get followee page total number - pid:%s' % (pid,))
                time.sleep(5)

        if fee_page_num == 0:
            print 'He/She does not follow any one.'
            return
        else:
            print 'Getting followee page 1 of %d...' % (fee_page_num,)
            followees = self.parser.parse_followees(html, pid, datetime.now())
            self.followee_list.extend(followees)  # followees cannot be None since it's been tested in self.get_followee_page_num(html)-> self.parser.parse_followee_page_num(html)
            if fee_page_num == 1:
                return
            for i in xrange(2, fee_page_num + 1):
                while True:
                    url = 'http://www.weibo.com/p/%s/follow?from=page_%s&wvr=6&mod=headfollow&page=%d#place' % (pid, pid[:6], i)
                    print 'Getting followee page %d of %d...' % (i, fee_page_num)
                    html = self.sess.get(url)
                    time.sleep(5)
                    followees = self.parser.parse_followees(html, pid, datetime.now())
                    if followees is None:  # dirty html
                        log.warning('Cannot parse followee page correctly - pid:%s' % (pid,))
                        time.sleep(5)
                        continue
                    self.followee_list.extend(followees)
                    break

