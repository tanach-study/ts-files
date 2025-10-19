from django.contrib.syndication.views import Feed
from django.db.models import Q
from django.utils.feedgenerator import Atom1Feed

from tssite.feeds.itunes import iTunesFeed
from tssite.models import Class


class RSSNachFeed(Feed):
    title = "Tanach Study"
    link = "/feeds/rss/tanach-study/"
    description = "Tanach Study is an initiative to promote the independent study of the books of Tanach‎ (Torah, Neviim and Ketuvim) through a web-based platform and weekly class. Our program aims to provide the Jewish community with immediate access to Torah knowledge in the form of a daily e-mail/podcast to complete and understand Neviim and Ketuvim in just 3 years. Tanach Study hopes to broaden Torah learning, to increase knowledge of our Jewish history, heighten our Yirat Shamayim, Ahavat Hashem, and strengthen our personal as well as our national identity."
    author_name = "Tanach Study"
    author_email = "info@tanachstudy.com"

    def items(self):
        return Class.objects.filter(
            Q(division='neviim_rishonim') | Q(division='neviim_aharonim') | Q(division='tere_assar') | Q(division='ketuvim')
        ).order_by('division_sequence', 'section_sequence', 'unit_sequence', 'part_sequence').order_by('date')

    def item_title(self, item):
        return str(item)

    def item_pubdate(self, item):
        return item.date

    def item_author_name(self, item):
        return item.teacher.__str__()

    def item_description(self, item):
        description = ''
        class_title = ''
        if item.division_sequence >= 2 or item.division_sequence <= 5:
            class_title = item.unit_title
            description = f'Sefer {item.section_title}'
            if item.section_sponsor:
                description = f'{description}<br />{item.section_sponsor}'

            description = f'{description}<br />Perek {item.unit}'
            if item.unit_sponsor:
                description = f'{description}<br />{item.unit_sponsor}'
        else:
            raise Exception(f'unsupported division {item.division}')

        if class_title != '':
            return f'<b>{class_title}</b><br />{description}<br /><audio controls=""><source src="https://cdn.tanachstudy.com/{item.audio}"></audio>'
        return f'{description}<br /><audio controls=""><source src="https://cdn.tanachstudy.com/{item.audio}"></audio>'

    def item_link(self, item):
        host = 'https://tanachstudy.com'
        return f'{host}{item.get_location()}'

    def item_enclosure_length(self, item):
        # TODO(joey): figure out how to set this properly
        return 0

    def item_enclosure_url(self, item):
        return "https://cdn.tanachstudy.com/" + str(item.audio)

    def item_enclosure_mime_type(self, item):
        return 'audio/mp3'


class AtomNachFeed(RSSNachFeed):
    feed_type = Atom1Feed
    subtitle = RSSNachFeed.title
    link = "/feeds/atom/tanach-study"


class PodcastNachFeed(AtomNachFeed):
    link = "/feeds/podcast/tanach-study"
    feed_type = iTunesFeed

    def feed_extra_kwargs(self, obj):
        return {
            'itunes_image_url': 'https://cdn.tanachstudy.com/assets/images/ts-podcast.jpg',
            'itunes_explicit': False,
            'itunes_categories': (('Religion & Spirituality', 'Judaism'), 'Education'),
        }
