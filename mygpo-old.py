#!/usr/bin/python

from __future__ import print_function, unicode_literals

import sys
import cStringIO
normout, normerr = sys.stdout, sys.stderr
sys.stdout = sys.stderr = cStringIO.StringIO()
from gpodder import api
client = api.PodcastClient()
oldout = sys.stdout
sys.stdout, sys.stderr = normout, normerr

essentials = ['12 Byzantine Rulers',
 "Dan Carlin's Hardcore History",
 'From Our Own Correspondent',
 'The History of Rome',
 'In Our Time With Melvyn Bragg',
 'Norman Centuries',
 'Thinking Allowed']


def update():
    todo = list(essentials)
    allcasts = client.get_podcasts()
    essentialpodcasts = [p for p in allcasts if p.title in essentials]
    otherpodcasts = [p for p in allcasts if p.title not in essentials]
    for p in essentialpodcasts:
        todo.remove(p.title)
    
    if len(todo) > 0:
        for title in todo:
            print("NOT FOUND:", repr(title))
            print('=' * 80)
    
    if otherpodcasts:
        print("SKIPPING:")
        for p in otherpodcasts:
            print('       ', p.title)
        print('-' * 80)
    
    print('{0:38} | {1:38}'.format("Podcast", "Last Episode"))
    print('-'*80)
    count = 0
    for podcast in essentialpodcasts:
        last_ep = podcast.get_episodes()[0]
        print('{0:38} | {1:38}'.format(podcast.title[:38], last_ep.title[:38]))
        #print '        "' + str(last_ep.title) + '"'
        podcast.update()
        for episode in podcast.get_episodes():
                if episode.is_new:
                    print('===', episode.title)
                    episode.download()
                    count += 1
    
    print('-'*80)
    print(count, 'episodes downloaded.')
    for title in todo:
        print('PODCAST', repr(title), 'NOT FOUND')
        
if __name__ == '__main__':
    update()
