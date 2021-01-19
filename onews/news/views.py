from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Article

class IndexView(generic.ListView):
    template_name = 'news/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        """Return the last 50 articles with title and body"""
        #return Article.objects.filter(self_has_title_and_body).order_by('-pub_date')[:50]
        return Article.objects.order_by('pub_date')[:50]


class DetailView(generic.DetailView):
    model = Article
    template_name = 'news/detail.html'
