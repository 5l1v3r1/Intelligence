"""
This is the (unofficial) Python API for malwr.com Website.
Using this code, you can retrieve recent analyses, domains, tags but also latest comments.
You can also submit files
"""
import hashlib

import re
import requests
import os
from bs4 import BeautifulSoup

from Feeds.feeder import Feeder
import Feeds.constants as C
from io import StringIO

class MalwrAPI(Feeder):
    """
        MalwrAPI Main Handler
    """
    session = None
    logged = False
    verbose = False


    def __init__(self, name,by,type,verbose=False, username=None, password=None, apikey=None):
        Feeder.__init__(self, type, name, by)
        self.verbose = verbose
        self.session = requests.session()
        self.username = username
        self.password = password
        self.apikey = apikey
#/account/login
    def login(self):
        """Login on malwr.com website"""
        if self.username and self.password:
            soup = self.request_to_soup(self.url + '/account/login')
            csrf_input = soup.find(attrs=dict(name='csrfmiddlewaretoken'))
            csrf_token = csrf_input['value']
            payload = {
                'csrfmiddlewaretoken': csrf_token,
                'username': u'{0}'.format(self.username),
                'password': u'{0}'.format(self.password)
            }
            login_request = self.session.post(self.url + "/account/login/",
                                              data=payload, headers=self.headers)

            if login_request.status_code == 200:
                self.logged = True
                return True
            else:
                self.logged = False
                return False

    def request_to_soup(self, url=None):
        """Request url and return the Beautifoul Soup object of html returned"""
        if not url:
            url = self.url

        req = self.session.get(url, headers=self.headers)
        soup = BeautifulSoup(req.content, "html.parser")
        return soup

    def display_message(self, s):
        """Display the message"""
        if self.verbose:
            print('[verbose] %s' % s)

    def get_latest_comments(self):
        """Request the last comments on malwr.com"""
        res = []
        soup = self.request_to_soup()
        comments = soup.findAll('div', {'class': 'span6'})[3]

        for comment in comments.findAll('tr'):
            infos = comment.findAll('td')

            infos_to_add = {
                'comment': infos[0].string,
                'comment_url': infos[1].find('a')['href']
            }
            res.append(infos_to_add)

        return res

    def get_recent_domains(self):
        """Get recent domains on index page
        Returns a list of objects with keys domain_name and url_analysis"""
        res = []
        soup = self.request_to_soup()

        domains = soup.findAll('div', {'class': 'span6'})[1]
        for domain in domains.findAll('tr'):
            infos = domain.findAll('td')
            infos_to_add = {
                'domain_name': infos[0].find('span').string,
                'url_analysis': infos[1].find('a')['href']
            }
            res.append(infos_to_add)

        return res

    def get_public_tags(self):
        """Get public tags on index page
        Return a tag list"""
        res = []
        soup = self.request_to_soup()

        tags = soup.findAll('div', {'class': 'span6'})[2]
        for tag in tags.findAll('a', {'class': 'tag-label'}):
            res.append(tag.string)

        return res

    def get_recent_analyses(self):

        res = []
        soup = self.request_to_soup()

        submissions = soup.findAll('div', {'class': 'span6'})[0]
        for submi