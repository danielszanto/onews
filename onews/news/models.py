from django.db import models
#from django.db.models import Model
import os
import uuid



def article_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/article_<id>/<filename>
    #return f"article_{instance.id}/{filename}"
    f, ext = os.path.splitext(filename)
    name = uuid.uuid4().hex
    return 'images/%s%s' % (name, ext)    
    
class Article(models.Model):
    title_text = models.CharField(max_length=200,blank=True,null=True)
    body_text = models.CharField(max_length=10000,blank=True,null=True)
    pub_date = models.DateTimeField('date published',auto_now_add=True)
    article_image = models.ImageField(upload_to=article_image_path, blank=True, null=True)
    title_text_insp = models.CharField(max_length=200,blank=True,null=True)
    body_text_insp = models.CharField(max_length=10000,blank=True,null=True)
    publish = models.BooleanField(default=False)
    def __str__(self):
        return self.title_text
    def has_title_and_body(self):
        return (None!=self.title_text and None!=self.body_text)    
    
#class ArticleImage(models.Model):
    #article = models.ForeignKey(Article, unique=True)
    #article_image = ImageField(upload_to=article_image_path, blank=True, null=True)
    