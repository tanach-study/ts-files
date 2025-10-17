from django.urls import path


from . import views
from tssite.feeds.nach import RSSNachFeed, AtomNachFeed, PodcastNachFeed
from tssite.feeds.talmud import RSSTalmudFeed, AtomTalmudFeed
from tssite.feeds.all import RSSAllFeed, AtomAllFeed
from tssite.feeds.schedule import ScheduleFeed

urlpatterns = [
    path('', views.index, name='index'),
    path('all', views.all, name='all'),
    path('feeds/rss/tanach-study', RSSNachFeed()),
    path('feeds/atom/tanach-study', AtomNachFeed()),
    path('feeds/podcast/tanach-study', PodcastNachFeed()),
    path('feeds/rss/talmud-study', RSSTalmudFeed()),
    path('feeds/atom/talmud-study', AtomTalmudFeed()),
    path('feeds/rss/all', RSSAllFeed()),
    path('feeds/atom/all', AtomAllFeed()),

    path('schedules', views.schedules, name='schedules'),
    path('schedule/<uuid:schedule_id>', views.schedule, name='schedule'),

    path('feeds/rss/schedule/<uuid:schedule_id>', ScheduleFeed())
]
