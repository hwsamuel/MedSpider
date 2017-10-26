# -*- coding: utf-8 -*-

from lxml import html
from lxml.html.soupparser import fromstring
from hashlib import sha1
from re import split
import requests, sys, math

reload(sys)
sys.setdefaultencoding('utf-8')

class Spidey:
    def _get_forums(self,url):
        page = requests.get(url)
        tree = html.fromstring(page.content)
        return tree.xpath("//a[@class='forumtitle']")

    def _get_discussions(self,url):
        page = requests.get(url)
        tree = html.fromstring(page.content)

        num_posts = int(tree.xpath("//div[@class='pagination']/text()")[0].strip().replace(' topics','').replace(' topic',''))
        pages = int(math.ceil(num_posts/100))+1
        
        discussions = []
        for i in range (1, pages+1):
            elements = tree.xpath("//a[@class='topictitle']")
            for element in elements:
                discuss_url = element.get('href')
                title = element.text
                new_discuss = [discuss_url, title]
                discussions.append(new_discuss)
            page = requests.get(url+'&start='+str(i*100))
            tree = html.fromstring(page.content)
        return discussions

    def _get_posts(self,url):
        page = requests.get(url)
        tree = html.fromstring(page.content)
        
        num_posts = tree.xpath("//div[@class='pagination']/text()")[0].encode('punycode')[:-1]
        parse_int = num_posts.find(' posts')
        if parse_int == -1:
            parse_int = num_posts.find(' post')
        num_posts = int(num_posts[:parse_int])
        pages = int(math.ceil(num_posts/15))+1
        
        posts = []
        for i in range (1, pages+1):
            elements = tree.xpath("//div[@class='postbody']")
            for element in elements:
                user = element.xpath(".//a[@class='username']")
                date = element.xpath(".//p[@class='author']/text()")
                date = ''.join(date).strip()
                if len(user) == 0:
                    user = element.xpath(".//a[@class='username-coloured']")
                user = user[0].text.strip()
                
                body = element.xpath(".//div[@class='content']/text()")
                body = ''.join(body).strip().replace('\t','').replace('\n','').replace('\r','').encode('punycode')[:-1]
                
                id = sha1(user+date+body).hexdigest()
                new_post = [id,user,date,body]
                posts.append(new_post)
            page = requests.get(url+'&start='+str(i*15))
            tree = html.fromstring(page.content)
        return posts

    def crawl(self,out_file):
        base = 'https://www.doctorslounge.com/forums/'
        main_url = base

        forums = self._get_forums(main_url)

        f = open(out_file, 'w')
        f.write('forum_id\tforum_name\tdiscussion_id\tdiscussion_title\tdiscussion_url\tpost_id\tposted_date\tusername\tcontent\n')
        
        for forum in forums:
            forum_url = base+forum.get('href')
            forum_name = forum.text
            forum_id = sha1(forum_url).hexdigest()

            discussions = self._get_discussions(forum_url)
            for discussion in discussions:
                discuss_url = base+discussion[0]
                discuss_title = discussion[1]
                discuss_id = sha1(discuss_url).hexdigest()
                
                posts = self._get_posts(discuss_url)
                for post in posts:
                    post_id = post[0]
                    post_user = post[1]
                    post_date = post[2]
                    post_content = post[3]
                    f.write(forum_id+'\t'+forum_name+'\t'+discuss_id+'\t'+discuss_title+'\t'+discuss_url+'\t'+post_id+'\t'+post_date+'\t'+post_user+'\t'+post_content+'\n')
        f.close()

class TestSpidey(object):
    def test_get_forums(self):
        assert len(Spidey()._get_forums('https://www.doctorslounge.com/forums/')) == 96
        
    def test_get_discussions1(self):
        assert len(Spidey()._get_discussions('https://www.doctorslounge.com/forums/viewforum.php?f=60')) == 133
    
    def test_get_discussions2(self):
        assert len(Spidey()._get_discussions('https://www.doctorslounge.com/forums/viewforum.php?f=62')) == 604
        
    def test_get_posts1(self):
        assert len(Spidey()._get_posts('https://www.doctorslounge.com/forums/viewtopic.php?f=62&t=40085')) == 2
    
    def test_get_posts2(self):
        assert len(Spidey()._get_posts('https://www.doctorslounge.com/forums/viewtopic.php?f=62&t=5528')) == 17
    
if __name__ == '__main__':
    Spidey().crawl('doctorslounge.csv')