#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
一个简单的豆瓣图书前250爬虫
Author: eric.guo email:gyc567@126.com
Date: 2016-08-27
Language: Python2.7.10

"""
import string
import re
import urllib2
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class DouBanSpider(object):
    """类的简要说明
    本类主要用于抓取豆瓣阅读Top前250的书籍的名称

    Attributes:
        page: 用于表示当前所处的抓取页面
        cur_url: 用于表示当前争取抓取页面的url
        datas: 存储处理好的抓取到的电影名称
        _top_num: 用于记录当前的top号码
    """

    def __init__(self):
        self.page = 1
        self.cur_url = "https://book.douban.com/top250?start=0"
        # self.cur_url = "http://movie.douban.com/top250?start={page}&filter=&type="
        # self.cur_url = "https://read.douban.com/reader/ebook/1296661/"
        self.datas = []
        self._top_num = 1
        print "豆瓣电影爬虫准备就绪, 准备爬取数据..."

    def get_page(self, cur_page):
        """
        根据当前页码爬取网页HTML
        Args:
            cur_page: 表示当前所抓取的网站页码
        Returns:
            返回抓取到整个页面的HTML(unicode编码)
        Raises:
            URLError:url引发的异常
        """
        url = self.cur_url
        try:
            my_page = urllib2.urlopen(url.format(page=(cur_page - 1) * 25)).read().decode("utf-8")
            # print "page content-->"+my_page
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print "The server couldn't fulfill the request."
                print "Error code: %s" % e.code
            elif hasattr(e, "reason"):
                print "We failed to reach a server. Please check your url and read the Reason"
                print "Reason: %s" % e.reason
        return my_page

    def find_title(self, my_page):
        """
        通过返回的整个网页HTML, 正则匹配前250的书籍名称

        Args:
            my_page: 传入页面的HTML文本用于正则匹配
        """
        temp_data = []
        # movie_items = re.findall(r'<span.*?class="title">(.*?)</span>', my_page, re.S)

        movie_items = re.findall(r'(?<=&#34; title=").*?(?=")', my_page, re.S)
        for index, item in enumerate(movie_items):
            if item.find("&nbsp") == -1:
                temp_data.append("Top" + str(self._top_num) + " " + item)
                self._top_num += 1
        self.datas.extend(temp_data)

    def start_spider(self):
        """
        爬虫入口, 并控制爬虫抓取页面的范围
        """
        while self.page <= 10:
            my_page = self.get_page(self.page)
            self.find_title(my_page)
            self.page += 1


def main():
    print """
        ###############################
            一个简单的豆瓣图书前250爬虫
            Author: eric.guo email:gyc567@126.com
            Date: 2016-08-27
        ###############################
    """
    my_spider = DouBanSpider()
    my_spider.start_spider()
    for item in my_spider.datas:
        print item

    with open("movieTitle.txt", "w+") as my_file:
            for page in my_spider.datas:
                my_file.write(page + "\n")

    print "豆瓣爬虫爬取结束..."


if __name__ == '__main__':
    main()
