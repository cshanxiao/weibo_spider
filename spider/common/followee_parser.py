# -*- coding: utf8 -*-
from bs4 import BeautifulSoup

from spider.common.common_parser import CommonParser
from spider.log import logging as log


class FolloweeParser(CommonParser):

    def parse_followee_page_num(self, html):
        """
        :param html:
        :return: followee page number, None if dirty html
        """
        soup = BeautifulSoup(html)
        scripts = soup.find_all('script')
        script = None
        for tmp_script in scripts:
            if 'follow_item S_line2' in tmp_script.text:
                # follow_item S_line2 denotes one followee
                script = tmp_script
                break

        if script is None:
            return 0

        # user followed someones
        html = self.covert_script_to_hmtl(script)
        if html is None:
            return None
        soup = BeautifulSoup(html)
        W_pages = soup.find('div', 'W_pages')
        if W_pages is not None:
            page_links = W_pages.find_all('a', attrs={'bpfilter': 'page'})
            return self.get_max_page_num(page_links)
        return 1

    def parse_followees(self, html, pid, timestamp):
        """
        :param html:
        :param pid:
        :param timestamp: crawled time
        :return: a list of followees
        """
        followees = []  # to return
        followee = {
            'uid': '',
            'fee_uid': '',
            'name': '',
            'profile_img': '',
            'description': '',
            'gender': '',
            'location': '',
            'app_source': '',
            'followee_num': '',
            'follower_num': '',
            'weibo_num': '',
            'is_vip': '0',
            'vip_level': '',
            'verified_type': '0',
            'is_daren': '0',
            'is_taobao': '0',  # deprecated
            'is_suishoupai': '0',  # deprecated
            'is_vlady': '0',
            'timestamp': ''
        }

        soup = BeautifulSoup(html)
        scripts = soup.find_all('script')
        script = None
        for scr in scripts:
            # follow_item S_line2 denotes for one follower
            if 'follow_item S_line2' in scr.text:
                script = scr
                break
        if script is None:
            return []  # no followees

        html = self.covert_script_to_hmtl(script)
        if html is None:
            return None  # dirty html

        soup = BeautifulSoup(html)
        followee_list = []
        for flist in soup.find_all('ul', 'follow_list'):
            # maybe there are two follow list one is the common one, the other is the recommendation one
            followee_list.extend(flist.find_all('li', 'follow_item S_line2'))

        for fee in followee_list:  # start to parse...
            followee['uid'] = pid[6:]
            followee['fee_uid'] = self.parse_followee_uid(fee)
            followee['name'] = self.parse_followee_name(fee)
            followee['profile_img'] = self.parse_followee_profile_img(fee)
            followee['description'] = self.parse_followee_description(fee)
            followee['gender'] = self.parse_followee_gender(fee)
            followee['location'] = self.parse_followee_location(fee)
            followee['app_source'] = self.parse_followee_app_source(fee)
            followee['followee_num'] = self.parse_followee_followee_num(fee)
            followee['follower_num'] = self.parse_followee_follower_num(fee)
            followee['weibo_num'] = self.parse_followee_weibo_num(fee)
            followee['vip_level'] = self.parse_followee_vip_level(fee)
            followee['verified_type'] = self.parse_followee_verified_type(fee)
            followee['is_daren'] = self.parse_followee_daren(fee)
            followee['is_vlady'] = self.parse_followee_vlady(fee)
            if followee['vip_level'] is not None:
                followee['is_vip'] = '1'
            followee['timestamp'] = timestamp
            # end parsing
            followees.append(followee)
            followee = self.reset_followee(followee)
        return followees

    def reset_followee(self, followee):
        """
        :param followee: a dict standing for a followee
        :return:
        """
        followee = {
            'uid': '',
            'fee_uid': '',
            'name': '',
            'profile_img': '',
            'description': '',
            'gender': '',
            'location': '',
            'app_source': '',
            'followee_num': '',
            'follower_num': '',
            'weibo_num': '',
            'is_vip': '0',
            'vip_level': '',
            'verified_type': '0',
            'is_daren': '0',
            'is_taobao': '0',
            'is_suishoupai': '0',
            'is_vlady': '0',
            'timestamp': ''
        }
        return followee

    def parse_followee_uid(self, followee):
        """
        :param followee: a li tag
        :return:
        """
        try:
            data = followee['action-data']
            data = data.split('&')
            for dt in data:
                if u'uid' in dt:
                    return dt.split('=')[-1]
            return None
        except Exception as e:
            log.error(e.message)
            return None

    def parse_followee_name(self, followee):
        """
        :param followee: a li tag
        :return:
        """
        try:
            data = followee['action-data']
            data = data.split('&')
            for dt in data:
                if u'fnick' in dt:
                    return dt.split('=')[-1]
            return None
        except Exception as e:
            log.error(e.message)
            return None

    def parse_followee_profile_img(self, followee):
        """
        :param followee: li tag
        :return:
        """
        try:
            dt = followee.find('dt', 'mod_pic')
            img = dt.find('a').find('img')
            return img['src']
        except Exception as e:
            log.error(e.message)
            return None

    def parse_followee_description(self, followee):
        """
        :param followee: li tag
        :return:
        """
        try:
            dd = followee.find('dd', 'mod_info S_line1')
            des = dd.find('div', 'info_intro')
            if des is None:
                return None
            return des.find('span').text
        except Exception as e:
            log.warning(e.message)
            return None

    def parse_followee_gender(self, followee):
        """
        :param followee: a li tag of html
        :return:
        """
        try:
            data = followee['action-data']
            data = data.split('&')
            for dt in data:
                if u'sex=' in dt:
                    return dt.split('=')[-1].upper()
            return None
        except Exception as e:
            log.warning(e.message)
            return None

    def parse_followee_location(self, followee):
        """
        :param followee: li
        :return:
        """
        try:
            dd = followee.find('dd', 'mod_info S_line1')
            loc = dd.find('div', 'info_add')
            return loc.find('span').text
        except Exception as e:
            log.warning(e.message)
            return None

    def parse_followee_app_source(self, followee):
        """
        :param followee: a li
        :return:
        """
        try:
            dd = followee.find('dd', 'mod_info S_line1')
            app = dd.find('div', 'info_from')
            return app.find('a', 'from').text
        except Exception as e:
            log.warning(e.message)
            return None

    def parse_followee_followee_num(self, followee):
        """
        :param followee:  list item of unordered list
        :return:
        """
        try:
            dd = followee.find('dd', 'mod_info S_line1')
            info = dd.find('div', 'info_connect')
            if info is None:
                return None  # recommended followees are without statistics information
            for i in info.find_all('span'):
                if u'关注' in i.text:
                    return i.find('a').text
            return None
        except Exception as e:
            log.warning(e.message)
            return None

    def parse_followee_follower_num(self, followee):
        """
        :param followee: li tag
        :return:
        """
        try:
            dd = followee.find('dd', 'mod_info S_line1')
            info = dd.find('div', 'info_connect')
            if info is None:
                return None  # recommended followees are without statistics information
            for i in info.find_all('span'):
                if u'粉丝' in i.text:
                    return i.find('a').text
            return None
        except Exception as e:
            log.warning(e.message)
            return None

    def parse_followee_weibo_num(self, followee):
        """
        :param followee: li tag
        :return:
        """
        try:
            dd = followee.find('dd', 'mod_info S_line1')
            info = dd.find('div', 'info_connect')
            if info is None:
                return None  # recommended followees are without statistics information
            for i in info.find_all('span'):
                if u'微博' in i.text:
                    return i.find('a').text
            return None
        except Exception as e:
            log.warning(e.message)
            return None

    def parse_followee_vip_level(self, followee):
        """
        :param followee: li tag of html
        :return:
        """
        try:
            dd = followee.find('dd', 'mod_info S_line1')
            icons = dd.find('div', 'info_name W_fb W_f14')
            vip = icons.find('a', attrs={'title': u'微博会员'})
            if vip is None:
                return None
            level = vip.find('em')['class'][-1][-1]
            return level
        except Exception as e:
            log.warning(e.message)
            return None

    def parse_followee_verified_type(self, followee):
        """
        :param followee: li tag
        :return:
        """
        try:
            dd = followee.find('dd', 'mod_info S_line1')
            icons = dd.find('div', 'info_name W_fb W_f14')
            types = icons.find_all('i')
            for tp in types:
                try:
                    title = tp['title']
                except KeyError:
                    continue
                if u'微博个人认证' in title:
                    return '1'
                elif u'微博机构认证' in title:
                    return  '2'
            return '0'
        except Exception as e:
            log.warning(e.message)
            return '0'

    def parse_followee_daren(self, followee):
        """
        :param followee: li tag
        :return:
        """
        try:
            dd = followee.find('dd', 'mod_info S_line1')
            icons = dd.find('div', 'info_name W_fb W_f14')
            daren = icons.find('i', attrs={'node-type': 'daren'})
            if daren is not None:
                return '1'
            else:
                return '0'
        except Exception as e:
            log.warning(e.message)
            return '0'

    def parse_followee_vlady(self, followee):
        """
        :param followee: a li of ul
        :return:
        """
        try:
            dd = followee.find('dd', 'mod_info S_line1')
            icons = dd.find('div', 'info_name W_fb W_f14')
            vlady = icons.find('i', 'W_icon icon_vlady')
            if vlady is not None:
                return '1'
            return '0'
        except Exception as e:
            log.warning(e.message)
            return '0'

