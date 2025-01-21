from django.urls import path

from . import views
from tssite.feeds.nach import RSSNachFeed, AtomNachFeed
from tssite.feeds.talmud import RSSTalmudFeed, AtomTalmudFeed
from tssite.feeds.all import RSSAllFeed, AtomAllFeed

urlpatterns = [
    path('', views.index, name='index'),
    path('all', views.all, name='all'),
    path('feeds/rss/tanach-study', RSSNachFeed()),
    path('feeds/atom/tanach-study', AtomNachFeed()),
    path('feeds/rss/talmud-study', RSSTalmudFeed()),
    path('feeds/atom/talmud-study', AtomTalmudFeed()),
    path('feeds/rss/all', RSSAllFeed()),
    path('feeds/atom/all', AtomAllFeed()),

    path('schedules', views.schedules, name='schedules'),
    path('schedule/<uuid:schedule_id>', views.schedule, name='schedule'),
]
