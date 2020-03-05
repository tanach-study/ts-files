from django.urls import path

from . import views
from tssite.feeds.nach import RSSNachFeed, AtomNachFeed

urlpatterns = [
    path('', views.index, name='index'),
    path('all', views.all, name='all'),
    path('feeds/rss/tanach-study', RSSNachFeed()),
    path('feeds/atom/tanach-study', AtomNachFeed()),
]
