import requests


class NGA(object):
    """bbs.nga.cc 精英玩家俱乐部API"""

    def __init__(self):
        self.http = requests.session()

        self.http.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; ONEPLUS A3010 Build/OPR1.170623.032; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.124 Mobile Safari/537.36',
            'X-USER-AGENT': 'Nga_Official/73001(OnePlus ONEPLUS A3010;Android 8.0.0)'
        })

    def t_list(self, fid, recommend=0, page=1):
        """
        帖子列表
        :return:
        :param fid: 论坛板块ID {往事杂谈: -7, }
        :param recommend: 是否精华贴 {0： 否， 1： 是}
        :param page: page
        """
        return self.response('http://bbs.nga.cn/app_api.php?__lib=subject&__act=list', data={
            'fid': fid,
            'stid': '0',
            'recommend': recommend,
            'page': page,
        })

    def t_list_hot(self, fid, days=1, page=1):
        """
        热门帖子
        :param fid: 论坛id
        :param days: 热帖周期 {1, 7, 30}
        :param page: page
        :return:
        """
        return self.response('http://bbs.nga.cn/app_api.php?__lib=subject&__act=hot', data={
            'fid': fid,
            'days': days,
            'page': page,
        })

    def t_content(self, tid, page=1):
        """
        帖子内容
        :param tid: 帖子ID
        :param page: page
        :return:
        """
        return self.response('http://bbs.nga.cn/app_api.php?__lib=post&__act=list', data={
            'page': page,
            'tid': tid
        })

    def u_content(self, uid):
        """
        用户信息
        :param uid: 用户uid
        :return:
        """
        return self.response('http://bbs.nga.cn/app_api.php?__lib=user&__act=detail', data={
            'uid': uid,
            '__ngaClientChecksum': '1fe72a148a1c3ae2c5b99e32d3c6cfd01526891914',  # 作用未知 可忽略
        })

    def u_reply(self, uid, page=1):
        """
        用户回帖列列表
        :param uid: 用户uid
        :param page: page
        :return:
        """
        return self.response('http://bbs.nga.cn/app_api.php?__lib=user&__act=replys', data={
            'uid': uid,
            'page': page,
        })

    def u_post(self, uid, page=1):
        """
        用户发帖列表
        :param uid: 用户ID
        :param page: page
        :return:
        """
        return self.response('http://bbs.nga.cn/app_api.php?__lib=user&__act=subjects', data={
            'uid': uid,
            'page': page,
        })

    def u_posts(self, uid, page=1):
        """
        用户发帖列表
        :param uid: 用户ID
        :param page: page
        :return:
        """
        x = self.http.post('http://bbs.nga.cn/app_api.php?__lib=user&__act=subjects', data={
            'uid': uid,
            'page': page,
        })

        return x.json()

    def response(self, url, data={}):
        """
        响应内容
        :param url:
        :param data:
        :return: json-encoded content
        """
        return self.http.post(url, data=data).json()