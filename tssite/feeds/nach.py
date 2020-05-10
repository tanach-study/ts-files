from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.db.models import Q
from tssite.models.common import Class

class RSSNachFeed(Feed):
    title = "Tanach Study"
    link = "/feeds/rss/tanach-study/"
    description = "Tanach Study is an initiative to promote the independent study of the books of Tanach‎ (Torah, Neviim and Ketuvim) through a web-based platform and weekly class. Our program aims to provide the Jewish community with immediate access to Torah knowledge in the form of a daily e-mail/podcast to complete and understand Neviim and Ketuvim in just 3 years. Tanach Study hopes to broaden Torah learning, to increase knowledge of our Jewish history, heighten our Yirat Shamayim, Ahavat Hashem, and strengthen our personal as well as our national identity."

    def items(self):
        return Class.objects.filter(
            Q(division='neviim_rishonim') | Q(division='neviim_aharonim') | Q(division='tere_assar') | Q(division='ketuvim')
        ).order_by('division_sequence', 'section_sequence', 'unit_sequence', 'part_sequence').order_by('date')[:10]

    def item_title(self, item):
        return str(item)

    def item_description(self, item):
        return item.get_location()

    def item_link(self, item):
        host = 'https://tanachstudy.com'
        return f'{host}{item.get_location()}'


class AtomNachFeed(RSSNachFeed):
    feed_type = Atom1Feed
    subtitle = RSSNachFeed.description
    link = "/feeds/atom/tanach-study"
