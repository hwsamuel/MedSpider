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
        return tree.xpath("//div[starts-with(@data-forum-key, 'Cat:OpenClinicalForum')]/div/h3/a")

    def _get_discussions(self,url):
        page = requests.get(url)
        tree = html.fromstring(page.content)

        discussions = []
        elements = tree.xpath("//div[@class='pluck-forums-main-discussion-inner-wrap']")
        for element in elements:
            discussion = element.xpath(".//p[@class='pluck-forums-cat-discussion-title']/a")[0]
            discuss_url = discussion.get('href').strip()
            name = discussion.get('title').strip()
            num_posts = element.xpath(".//div[@class='pluck-forums-main-discussion-posts-col']/p/text()")[0].strip()
            new_discuss = [discuss_url, name, num_posts]
            discussions.append(new_discuss)
        return discussions

    def _get_posts(self,url):
        page = requests.get(url)
        tree = html.soupparser.fromstring(page.content, features='html.parser')

        posts = []
        elements = tree.xpath("//div[contains(@class,'pluck-forums-main-forumpost-wrap')]")
        for element in elements:
            title = element.xpath(".//div[contains(@class,'pluck-forums-forumpost-title')]/text()")
            if len(title) == 0: # Parsing issue with getting blank title
                continue
            else:
                title = title[0].strip()

            body_raw = element.xpath(".//div[@class='pluck-forums-forumpost-text']")
            body = [p.text_content().strip() for p in body_raw][0].strip()
            user = element.xpath(".//div[@class='pluck-forums-forumpost-username']/a/text()")[0].strip()
            date_time = element.xpath(".//p[@class='pluck-forums-main-forumpost-timestamp']/a/text()")[0].strip()
            date = date_time.split(',')[0].strip()
            time = date_time.split(',')[1].strip()

            id = sha1(title+body+user+date+time).hexdigest()
            new_post = [id, date, time, user, title, body]
            posts.append(new_post)
        return posts

    def crawl(self,out_file):
        base = 'https://web.archive.org' 
        main_url = base+'/web/20160615110024/http://doc2doc.bmj.com/forumhome.html'

        forums = self._get_forums(main_url)
        
        f = open(out_file, 'w')
        f.write('post_id,discussion_id,forum_id,url,posted_date,posted_time,username,title,content\n')
        
        for forum in forums:
            forum_url = base+forum.get('href')
            name = forum.text
            forum_id = sha1(forum_url).hexdigest()

            discussions = self._get_discussions(forum_url)
            for discussion in discussions:
                discuss_url = discussion[0]
                name = discussion[1]
                num_posts = int(discussion[2])
                discuss_id = sha1(discuss_url).hexdigest()
                pages = int(math.ceil(num_posts/10))+1

                for i in range (1, pages+1):
                    page_url = discuss_url+'?plckForumPostOnPage='+str(i)
                    posts = self._get_posts(page_url)
                        
                    for post in posts:
                        post_id = post[0]
                        post_date = post[1]
                        post_time = post[2]
                        username = post[3]
                        title = post[4]
                        content = post[5].encode('punycode').replace('\n', '')
                        f.write(post_id+','+discuss_id+','+forum_id+','+discuss_url+','+post_date+','+post_time+','+username+','+title+','+content+'\n')
        f.close()

class TestSpidey(object):
    def test_get_forums(self):
        assert len(Spidey()._get_forums('https://web.archive.org/web/20160615110148/http://doc2doc.bmj.com/forumhome.html')) == 15
        
    def test_get_discussions(self):
        assert len(Spidey()._get_discussions('https://web.archive.org/web/20160615110304/http://doc2doc.bmj.com/forums/open-clinical_cardiology')) == 15
        
    def test_get_posts(self):
        assert len(Spidey()._get_posts('https://web.archive.org/web/20160615110304/http://doc2doc.bmj.com/forums/open-clinical_cardiology_effects-of-hot-bath-blood-pressure')) == 7
    
if __name__ == '__main__':
    Spidey().crawl('doc2doc.csv')