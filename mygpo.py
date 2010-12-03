#!/usr/bin/python2

from __future__ import print_function, unicode_literals

import sys
import cStringIO
normout, normerr = sys.stdout, sys.stderr
sys.stdout = sys.stderr = cStringIO.StringIO()
from gpodder import api
client = api.PodcastClient()
oldout = sys.stdout
sys.stdout, sys.stderr = normout, normerr

import futures
from functools import partial

def podcaster(podcast):
    title = podcast.title
    lastep = podcast.get_episodes()[0]
    podcast.update()
    neweps = [ep for ep in podcast.get_episodes() 
            if ep.is_new]
    return title, neweps, lastep

def episoder(title, episode):
    eptitle = episode.title
    episode.download()
    episode.is_downloaded = True
    episode.is_new = True
    return title, eptitle

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

    print('-'*80)
    if otherpodcasts:
        print("SKIPPING:")
        for p in otherpodcasts:
            print('       ', p.title)
        print('-' * 80)
    
    print('   {0:37} | {1:37}'.format('Podcast Title', 'Last Episode'))
    print('-' * 80)
    
    with futures.ThreadPoolExecutor(8) as executor:
        neweps = []
        for title, eps, lastep in executor.run_to_results(
                [partial(podcaster, ep) for ep in essentialpodcasts]):
            for ep in eps:
                neweps.append((title, ep))
            if eps or True:
                print(('{0:2d} {1:37} | {2:37}'.format(
                    len(eps), title, lastep.title))[:80])
    
    print('='*80)
    if neweps:
        print('   {0:37} | Downloaded Episode ({1})'.format(
            'Podcast Title', len(neweps)))
        print('-' * 80)
    with futures.ThreadPoolExecutor(8) as executor:
        for title, eptitle in executor.run_to_results(
                [partial(episoder, title, ep) for title, ep in neweps]):
            print('   {0:37} | {1:37}'.format(title[:37], 
                eptitle[:37]))

if __name__ == '__main__':
    update()
