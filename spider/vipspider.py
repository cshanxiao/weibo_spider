# -*- coding: utf8 -*-
u'''
@summary:
@author: Administrator
@date: 2016年3月14日
'''
from spider.log import logging
from spider.weibo import Weibo
import redis

class VipSpider(Weibo):
    def __init__(self):
        Weibo.__init__(self)

    def get_followees(self, pid):
        url = 'http://www.weibo.com/p/' + pid + '/follow?from=page_' + pid[:6] + '&wvr=6&mod=headfollow#place'
        while True:
            fetcher = self.fetchers[self.main_fetcher]
            html = open_url(fetcher, url)

            uid = self.parser.parse_uid(html)
            if uid == -1:
                self.ban_account()
                continue
            elif self.parser.is_visitor(html) is True:
                self.reset_account()
                continue

            fee_page_num = self.get_followee_page_num(html)
            if fee_page_num is not None:
                break
            else:
                log.warning('Cannot get followee page total number - pid:%s' % (pid,))
                time.sleep(random.randint(Config.SLEEP_WHEN_EXCEPTION, 2 * Config.SLEEP_WHEN_EXCEPTION))

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
                    html = open_url(fetcher, url)
                    time.sleep(random.randint(Config.SLEEP_BETWEEN_2FPAGES, 2 * Config.SLEEP_BETWEEN_2FPAGES))
                    followees = self.parser.parse_followees(html, pid, datetime.now())
                    if followees is None:  # dirty html
                        log.warning('Cannot parse followee page correctly - pid:%s' % (pid,))
                        time.sleep(random.randint(Config.SLEEP_WHEN_EXCEPTION, 2 * Config.SLEEP_WHEN_EXCEPTION))
                        continue
                    self.followee_list.extend(followees)
                    break

