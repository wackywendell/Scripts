#!/usr/bin/python

from gpodder import api

client = api.PodcastClient()

essentials = ['12 Byzantine Rulers: The History of The Byzantine Empire',
 "Dan Carlin's Hardcore History",
 'From Our Own Correspondent',
 'The History of Rome',
 'In Our Time With Melvyn Bragg',
 'Norman Centuries | A Norman History Podcast by Lars Brownworth',
 'Thinking Allowed']


def update():
    todo = list(essentials)
    count = 0
    for podcast in client.get_podcasts():
        if podcast.title not in todo:
            print '   ', 'skipping', podcast.title
            continue
        todo.remove(podcast.title)
        print 'updating', podcast.title
        podcast.update()
        for episode in podcast.get_episodes():
                if episode.is_new:
                    print '===', episode.title
                    episode.download()
                    count += 1

    print count, 'episodes downloaded.'
    for title in todo:
        print 'PODCAST', repr(title), 'NOT FOUND'
        
update()