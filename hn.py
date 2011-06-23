'''
Phenny module to make Phenny fetch the highest scoring HN article and post 
it for discussion.
'''
import urllib, json, random, time
from datetime import datetime as dt



REFRESH_SECONDS = 60 * 60 # 30 minutes
MAX_HISTORY_SIZE = 10



def parse_hn(response):
    '''
    Default function handles Hacker News JSON output.
    
    @param response: A response object from urllib
    '''
    try:
        return [z[1] for z in sorted([(
            x['points'], 
            x['url']
        ) for x in json.loads(response.read())['items']])]
    except Exception as e:
        print e

def parse_reddit(response):
    '''
    Handles reddit JSON.
    '''
    try:
        links = json.loads(response.read())['data']['children']
        return [z[1] for z in sorted([(
            x['data']['score'], 
            x['data']['url']
        ) for x in links])]
    except Exception as e:
        print e


# These are sources for links. The dictionary key should be a short 
# name for the given source. The values are 2-tuples consisting of 
# the URL from which to fetch data and a function that can turn 
# the response object into a sorted list of links. Links will be 
# taken from the end of the list first.
_sources = {}

# These are phrases the bot will use to present a link. Any string will 
# work so long as it has a single %s where the link URL will go.
_link_phrases = [
    'Hey everyone, we should talk about this: %s',
    'Check out this link I found... %s',
    'This is definitely the most important thing I have seen all day: %s',
    'Anyone else see this? %s',
    'This should be the new topic of discussion: %s',
    'Ready? %s Now discuss amongst yourselves!',
]
# These are phrases the bot uses when it is asked to repeat a link.
_repeat_phrases = [
    #TODO Use this
]



# These are for maintaining state between triggers. Nothing to see here, 
# move along.
_last_run = dt(1000,1,1,0,0,0) # Long time ago
_last_urls = []



def register_source(name, url, func):
    '''
    Register a new link source with the bot.
    
    @param name: The short name for the source being added
    @param url: The URL to fetch data from
    @param func: The function to call with the response from the URL
    '''
    global _sources
    
    try:
        if name not in _sources:
            _sources[name] = (url, func)
            return 'Success'
        else:
            return 'Unavailable'
    except Exception as e:
        print e



# Some fun default sources. Defaults might not be kid-friendly.
register_source(
    'hn', 
    'http://api.ihackernews.com/page', 
    parse_hn
)
register_source(
    'reddit', 
    'http://www.reddit.com/.json', 
    parse_reddit
)
register_source(
    'r/programming', 
    'http://www.reddit.com/r/programming/.json', 
    parse_reddit
)
register_source(
    'r/nsfw',
    'http://www.reddit.com/r/nsfw/.json',
    parse_reddit
)
register_source(
    'r/drugs',
    'http://www.reddit.com/r/drugs/.json',
    parse_reddit
)



def _get_link():
    global MAX_HISTORY_SIZE
    global _last_urls
    global _sources
    
    try:
        source = random.choice(_sources.keys())
                
        resp = urllib.urlopen(url=_sources[source][0])
        urls = _sources[source][1](resp)
        
        url = urls.pop()
        while url in _last_urls:
            url = urls.pop()
        
        _last_urls.insert(0, url)
        if len(_last_urls) > MAX_HISTORY_SIZE:
            _last_urls.pop()
        
        return {'source': source, 'url': url}
    except Exception as e:
        print e

def _say_link(ph, source, url):
    global _link_phrases
    
    try:
        ph.say(random.choice(_link_phrases) % url + ' (%s)' % source)
    except Exception as e:
        print e



def hn(ph, data):
    global REFRESH_SECONDS
    global _last_run
    
    try:
        now = dt.now()
        
        if (now - _last_run).seconds >= REFRESH_SECONDS:
            _last_run = now
            
            # Sleep for a couple seconds to seem more natural
            time.sleep(random.randint(1, 15))
            
            _say_link(ph=ph, **_get_link())
    except Exception as e:
        # Because Phenny blasts exceptions into the channel
        print e

hn.rule = r'.*'
hn.priority = 'medium'
hn.thread = True



def repeat(ph, data):
    global _last_urls
    
    try:
        if _last_urls:
            ph.say('%s: Pay closer attention next time... %s' % (
                data.nick, 
                _last_urls[0],
            ))
        else:
            ph.say('Hold your horses, let me think!')
            
    except Exception as e:
        print e
        
repeat.rule = r'$nickname: repeat link'
repeat.priority = 'medium'
repeat.thread = False



def new_link(ph, data):
    try:
        _say_link(ph=ph, **_get_link())
    except Exception as e:
        print e

new_link.rule = r'$nickname: new link'
new_link.priority = 'medium'
new_link.thread = False



