## Sheduler
## Populates the Article model
## TODO: Add images

from news.models import Article
from apscheduler.schedulers.background import BackgroundScheduler

from datetime import datetime
import feedparser
import re
import requests
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


rss_address = "https://theconversation.com/au/articles.atom"
txt_ai_details = {
    'address' : 'https://api.deepai.org/api/text-generator',
    'key' : 'b7ee7238-69ac-4c10-a2c6-4829a2438443',
    'feed_txt_len' : 800
    }



#Inputs source article text into DeepAI
#DeepAI continues where source text left off
#New text is appended to input
#(DeepAI is like OpenAI - but much worse)
def generate_body_text(txt):
    r = requests.post(
        txt_ai_details['address'],
        data={
            'text': txt
        },
        headers={'api-key': txt_ai_details['key']}
    )
    if r.ok and 'output' in r.json():
        logger.info("Successfully generated text")
        return True, r.json()['output']
    else:
        return False, "No output, try updating pyOpenSSL. Or the server did not like the input. Or try again later"

#the generated text from generate_body_text begins mid sentence
#find_next_sentence removes the first, incomplete sentence and returns result
def find_next_sentence(txt):
    try:
        return txt[txt.index('. ')+2:]
    except:
        return txt
    
#Searches for a sentence between 20 and 250 chars long to use as a title
#If no such sentence exists then returns the first 100 chars
def get_title_text(txt):
    tt = re.search(r'[^\.]{20,250}',txt,flags=0)
    if tt: return tt.group(0)
    else: return txt[0:100]
    
    
##Creates new articles from the originals
##looks for objects that have source text
##but not yet populated with gen text
##will only do one article at a time, won't spam API
def get_generated_text():
    articles = Article.objects.all()
    for o in articles:
        if None == o.body_text and None != o.body_text_insp:
            text_generate_success, text_generate_output = generate_body_text(o.body_text_insp)
            if text_generate_success and len(text_generate_output)>len(o.body_text_insp):
                tt = text_generate_output[len(o.body_text_insp):]
                o.body_text = find_next_sentence(tt)
                o.title_text = get_title_text(o.body_text)
                o.publish = True
                o.save()
                logger.info("Article id= %d populated with generated text",o.id)
                return
            else:
                logger.warning(text_generate_output) 
        elif None == o.body_text_insp:
            logger.warning("Article id= %d has no body_text_insp, this should not happen",o.id)
            
        
##Downloads news articles from RSS feed
def get_convos():
    to_write = []
    qp = []
    articles = Article.objects.all()
    fd = feedparser.parse(rss_address)
    if 'entries' in fd:
        for e in fd.entries:
            already_got = False
            for o in articles:
                if (e.title == o.title_text_insp):
                    already_got = True
            if(already_got == False):
                if len(e.summary) < txt_ai_details['feed_txt_len']: qpoint = len(e.summary)
                else: qpoint = txt_ai_details['feed_txt_len']
                body_insp = re.sub('<[^>]*>',"",e.summary[0:qpoint])                
                #body_insp = re.sub('<[^>]*>',"",e.summary[0:txt_ai_details['feed_txt_len']]) ##API is very unreliable, can't tell if this is breaking it or not. More testing required
                to_write.append(Article(title_text_insp=e.title,body_text_insp = body_insp))
        for tw in to_write:
            tw.save()
            logger.info("Article id= %d created",tw.id)
    else:
        logger.error("RSS Feed not returned")
        

        

def start():
    get_convos()
    get_generated_text()
    scheduler = BackgroundScheduler()
    logger.info("Adding job: get_convos...")
    scheduler.add_job(get_convos, 'interval', hours=2)
    logger.info("Adding job: get_generated_text...")
    scheduler.add_job(get_generated_text, 'interval', minutes=5)
    logger.info("Starting scheduler...")    
    scheduler.start()