from django.test import TestCase

from .models import Article

class ArticleModelTests(TestCase):
    
    def test_article_created_but_not_populated(self):
        #Article created with source material from RSS (scheduler.get_convos)
        #But scheduler.get_generated_text has not yet run for this object
        unpopulated_article = Article(title_text_insp='a',body_text_insp='a')
        self.assertIs(unpopulated_article.has_title_and_body(), False)
        
    def test_article_created_and_populated(self):
        #Article created with source material from RSS (scheduler.get_convos)
        #But scheduler.get_generated_text has not yet run for this object
        unpopulated_article = Article(title_text_insp='a',body_text_insp='a',title_text='a',body_text='a')
        self.assertIs(unpopulated_article.has_title_and_body(), True)    
