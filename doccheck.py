# -*- coding: utf-8 -*-

from lxml import html
from lxml.html.soupparser import fromstring
from hashlib import sha1
from re import split
import requests, sys, math

reload(sys)
sys.setdefaultencoding('utf-8')

# You have to create a medic-related account on DocCheck
# Update your login details in doccheck_auth.py
from doccheck_auth import *

class Spidey:
    def auth(self):
        username = DOCCHECK_USERNAME
        password = DOCCHECK_PWD
        session_requests = requests.session()
        token_url = "http://www.doccheck.com/com/core/user/loginpage/"
        login_url = "http://www.doccheck.com/com/user/login"
        result = session_requests.get(token_url)
        tree = html.fromstring(result.text)
        authenticity_token = list(set(tree.xpath("//input[@name='returnUrlEnc']/@value")))[0]
        payload = {"username": username, "password": password, "returnUrlEnc": authenticity_token}
        session_requests.post(login_url, data = payload, headers = dict(referer=login_url))
        return session_requests
        
    def _get_discussions(self,url):
        discussions = []
        page = requests.get(url)
        tree = html.fromstring(page.content)
        
        num_discussions = tree.xpath("//span[@class='paginationNumericNum']/text()")
        if len(num_discussions) == 0:
            return discussions
        num_discussions = num_discussions[0].encode('punycode')[:-1].strip()
        parse_int = num_discussions.find(' ')
        num_discussions = int(num_discussions[parse_int+1:])
        
        for i in range(1, num_discussions+1):
            elements = tree.xpath("//div[@class='askQuestionListingEntry']")
            for element in elements:
                item = element.xpath(".//div[@class='askQuestionListingEntryTitle']/a")[0]
                furl = item.get('href')
                num_replies = element.xpath(".//div[@class='askQuestionListingAnswerCountContainer']/a/span/text()")[0]
                ftitle = item.text
                discussions.append([furl,ftitle,int(num_replies)])
            page = requests.get(url+'/home/index/page/'+str(i+1))
            tree = html.fromstring(page.content)
        return discussions
        
    def _get_posts(self,url,srequests=None):
        posts = []
        if srequests == None:
            srequests = self.auth()
        page = srequests.get(url, headers = dict(referer = url))
        tree = html.fromstring(page.content)
        
        question = tree.xpath("//div[@class='askQuestionContentContainer']/p/text()")
        question = ''.join(question).replace('\n',' ').replace('\r',' ').replace('\t',' ').strip()
        date = tree.xpath("//div[@class='askQuestionContentOwnerAndCreatedContainer']/p[1]/text()")
        date = ''.join(date)[3:13]
        author = tree.xpath("//div[@class='askQuestionContentOwnerAndCreatedContainer']/p[1]/a/text()")
        if len(author) == 0:
            author = "Unknown"
        else:
            author = author[0]
        role = tree.xpath("//div[@class='askQuestionContentOwnerAndCreatedContainer']/p[1]/span/text()")
        if len(role) == 0:
            role = "Unspecified"
        else:
            role = role[0].strip()
        posts.append([question, date, author, role])
        
        answers = tree.xpath("//div[@class='askAnswerEntryRight']")
        for element in answers:
            answer = element.xpath(".//div[@class='askAnswerEntryBody']/p/text()")
            if len(answer) == 0:
                answer = ""
            else:
                answer = answer[0].strip()
            replier = element.xpath(".//span[@class='dcAnswerPerformerName']/a/text()")
            if len(replier) == 0:
                replier = "Unknown"
            else:
                replier = replier[0]
            date = element.xpath(".//div[@class='dcAnswerUserInfoContainer']/text()")
            date = ''.join(date).strip()
            parse = date.find('at')+3
            date = date[parse:parse+10]
            rrole = element.xpath(".//div[@class='dcAnswerUserInfoContainer']/span[3]/text()")
            if len(rrole) == 0:
                rrole = "Unspecified"
            else:
                rrole = rrole[0].strip()
                rrole = rrole[1:len(rrole)-1]
            posts.append([answer, date, replier, rrole])
        return posts

    def crawl(self,out_file):
        base = 'http://www.doccheck.com/com/ask'
        main_url = base
        sreq = self.auth()
        
        f = open(out_file, 'w')
        f.write('discussion_id\tdiscussion_title\tdiscussion_url\tpost_date\tpost_author\tauthor_role\tcontent\n')
        
        discussions = self._get_discussions(main_url)
        for discussion in discussions:
            discuss_url = discussion[0]
            discuss_title = discussion[1]
            discuss_num_replies = discussion[2]
            if discuss_num_replies == 0: # Ignore discussions without replies
                continue
            discuss_id = sha1(discuss_url).hexdigest()
            
            posts = self._get_posts(discuss_url,sreq)
            for post in posts:
                post_content = post[0]
                post_date = post[1]
                post_author = post[2]
                author_role = post[3]
                f.write(discuss_id+'\t'+discuss_title+'\t'+discuss_url+'\t'+post_date+'\t'+post_author+'\t'+author_role+'\t'+post_content+'\n')
        f.close()

class TestSpidey(object):
    def test_get_discussions(self):
        assert len(Spidey()._get_discussions('http://www.doccheck.com/com/ask')) == 205
        
    def test_get_posts1(self):
        assert len(Spidey()._get_posts('http://www.doccheck.com/com/ask/question/view/id/592759/')) == 6
    
    def test_get_posts2(self):
        assert len(Spidey()._get_posts('http://www.doccheck.com/com/ask/question/view/id/593057/')) == 3
    
if __name__ == '__main__':
    Spidey().crawl('doccheck.csv')