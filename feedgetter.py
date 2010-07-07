#!/usr/bin/python

import feedparse
from future import Future

class podcast:
    def __init__(self, url, mp3func):
        self.url = None
    
    def 

def main(plist):
    # initiate the downloads of all the RSS feeds
    fs = [Future(feedparse.parse, pcast.url) for pcast in plist]
    for f in fs:
        # wait for this RSS to finish downloading before we get
        # all the entries
        pcast = f() # wait