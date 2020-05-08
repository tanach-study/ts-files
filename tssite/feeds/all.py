from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.db.models import Q
from tssite.models import TalmudStudy, Class


class RSSAllFeed(Feed):
    title = "Tanach Study Daily Updates"
    link = "/feeds/rss/all"
    description = "Description of Tanach Study Daily Updates"

    def items(self):
        items = []
        for i in TalmudStudy.objects.all().order_by('-date')[:500]:
            items.append(("talmud", i))

        others = Class.objects.exclude(date__isnull=True).order_by('division_sequence', 'section_sequence', 'unit_sequence', 'part_sequence').order_by('date')[:500]

        for i in others:
            items.append(("other", i))
        return items

    def item_title(self, item):
        return str(item[1])

    def item_pubdate(self, item):
        return item[1].date

    def item_author_name(self, item):
        return item[1].teacher.__str__()

    def item_description(self, tup):
        description = ""
        item = tup[1]
        if tup[0] == "talmud":
            title = str(item)
            seder = item.seder.title()
            masechet = item.masechet.title()
            teacher = str(item.teacher)
            link = item.get_location()
            seder_sponsor = '' if not item.seder_sponsor else item.seder_sponsor
            masechet_sponsor = '' if not item.masechet_sponsor else item.masechet_sponsor
            daf_sponsor = '' if not item.daf_sponsor else item.daf_sponsor

            description = f'{title}<br /><br />This daf in {seder} is taught by {teacher}.'
            if seder_sponsor:
                description = f'{description}<br /><br />Seder {seder}<br />{seder_sponsor}'
            else:
                description = f'{description}<br /><br />Seder {seder}<br /><i>Sponsorship available</i>'
            if masechet_sponsor:
                description = f'{description}<br /><br />Masechet {masechet}<br />{masechet_sponsor}'
            else:
                description = f'{description}<br /><br />Masechet {masechet}<br /><i>Sponsorship available</i>'
            if daf_sponsor:
                description = f'{description}<br /><br />Daf {item.daf}<br />{daf_sponsor}'
            else:
                description = f'{description}<br /><br />Daf {item.daf}<br /><i>Sponsorship available</i>'
        if tup[0] == "other":
            description = str(item)
        return description

    def item_link(self, tup):
        host = 'https://tanachstudy.com'
        return f'{host}{tup[1].get_location()}'

    def item_enclosure_url(self, item):
        return f'https://cdn.tanachstudy.com/{item[1].audio}'

    item_enclosure_mime_type = 'audio/mpeg'


class AtomAllFeed(RSSAllFeed):
    feed_type = Atom1Feed
    subtitle = RSSAllFeed.description
    link = "/feeds/atom/all"
