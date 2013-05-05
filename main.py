#!/usr/bin/env python
# THIS IS USED AS AN EXAMPLE OF EXPLORING THE PANDORA JSON URLS. 
# NO WARRANTY IS GIVEN OF ANY KIND FOR THE DATA OUTPUT FROM USING THIS.
# SIMULTANEOUSLY HITTING THE PANDORA API IS PROBABLY PROHIBITTED.

import webapp2
import os
import sys
import json
sys.path.insert(0, 'libs')
from bs4 import BeautifulSoup
from google.appengine.api import urlfetch
from google.appengine.api import memcache
from google.appengine.ext.webapp import template


def getArtist(name):
    """
    RETURN PANDORA INFO ON GIVEN ARTIST
    ARGS:
        name = artist name e.g. Snoop Dogg etc.
    """
    if memcache.get(name):
        return memcache.get(name)
    else:
        url = 'http://www.pandora.com/json/music/artist/' + name
        data = urlfetch.fetch(url, headers={
                              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31'}).content
        memcache.add(name, data, 180)
        return data


def Popular():
    """
    RETURN POPULAR ARTITSTS FROM MTV WITH PANDORA URL AND ARTIST IMAGERY
    """
    if memcache.get('popular'):
        return memcache.get('popular')
    else:
        url = 'https://www.mtv.com/artists/popular/'
        html = urlfetch.fetch(url, validate_certificate=False, headers={
                              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31'}).content
        s = BeautifulSoup(html)
        html = []
        artists = s.findAll('div', {'class': 'title multiline'})
        for i in artists:
            artist = i.text
            html.append(i.text)
        for i in html[:30]:
            try:
                explorer = json.loads(getArtist(
                    i))['artistExplorer']['similar']
                for similar in explorer:
                    html.append(similar['@name'])
            except:
                pass
        d = []
        for i in list(set(html)):
            try:
                explorer = json.loads(getArtist(i))['artistExplorer']
                d.append({'artist': i, 'art': explorer[
                         '@artUrl'], 'pandora_url': explorer['@shareUrl']})
            except:
                pass
        memcache.set('popular', {'data': d})
        return {'data': d}


class IndexHandler(webapp2.RequestHandler):
    def get(self):
        """
            INDEX HANDLER: main page e.g. www.host.com
        """
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, Popular()))


class MusicHandler(webapp2.RequestHandler):
    def get(self):
        """
        MUSIC HANDLER: Returns page for given artist e.g. www.host.com/music?artist=coldplay
        """
        artist = self.request.get("artist")
        self.response.headers.add_header(
            'Content-Type', "application/javascript; charset=utf-8")
        self.response.write(getArtist(artist))


# SET APP VARIABLES
app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/music', MusicHandler)
], debug=True)
