'''
Phenny module to make Phenny fetch the highest scoring HN article and post 
it for discussion.
'''
import os, urllib, json
from datetime import datetime as dt



REFRESH_SECONDS = 60 * 15 # 15 minutes
MAX_HISTORY_SIZE = 10

last_run = dt(1000,1,1,0,0,0) # Long time ago
last_urls = []



def hn(ph, data):
    global REFRESH_SECONDS
    global MAX_HISTORY_SIZE
    global last_run
    global last_urls
    
    try:
        now = dt.now()
        
        if (now - last_run).seconds >= REFRESH_SECONDS:
            last_run = now
            
            # For finding max votes
            def get_most_popular(items):
                def max_item(a, b):
                    if int(a['points']) > int(b['points']):
                        return a
                    else:
                        return b
                pop = reduce(max_item, items)
                items.remove(pop)
                return pop
                
            resp = urllib.urlopen(url='http://api.ihackernews.com/page')
            items = json.loads(resp.read())['items']
            
            url = get_most_popular(items)['url']
            while url in last_urls:
                url = get_most_popular(items)['url']
            
            last_urls.insert(0, url)
            if len(last_urls) > MAX_HISTORY_SIZE:
                last_urls.pop()
            
            ph.say('Hey everyone, we should talk about this: %s' % url)
            
    except Exception as e:
        # Because Phenny blasts exceptions into the channel
        print e

hn.rule = r'.*'
hn.priority = 'medium'
hn.thread = False



def repeat(ph, data):
    global last_urls
    
    try:
        if last_urls:
            ph.say('Sure %s, I love repeating myself... %s' % (
                data.nick, 
                last_urls[0],
            ))
        else:
            ph.say('Hold your horses, let me think!')
            
    except Exception as e:
        print e
        
repeat.rule = r'$nickname: repeat hn'
repeat.priority = 'medium'
repeat.thread = False
