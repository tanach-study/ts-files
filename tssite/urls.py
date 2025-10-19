from django.urls import path

from tssite.feeds.all import AtomAllFeed, RSSAllFeed
from tssite.feeds.nach import AtomNachFeed, PodcastNachFeed, RSSNachFeed
from tssite.feeds.schedule import ScheduleFeed
from tssite.feeds.talmud import AtomTalmudFeed, RSSTalmudFeed

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("all", views.all, name="all"),
    path("feeds/rss/tanach-study", RSSNachFeed()),
    path("feeds/atom/tanach-study", AtomNachFeed()),
    path("feeds/podcast/tanach-study", PodcastNachFeed()),
    path("feeds/rss/talmud-study", RSSTalmudFeed()),
    path("feeds/atom/talmud-study", AtomTalmudFeed()),
    path("feeds/rss/all", RSSAllFeed()),
    path("feeds/atom/all", AtomAllFeed()),
    path("schedules", views.schedules, name="schedules"),
    path("schedule/<uuid:schedule_id>", views.schedule, name="schedule"),
    path("feeds/rss/schedule/<uuid:schedule_id>", ScheduleFeed()),
]
