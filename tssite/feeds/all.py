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
            items.append((i.division, i))
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
        title = str(item)
        teacher = str(item.teacher)
        if tup[0] == "talmud":
            seder = item.seder.title()
            masechet = item.masechet.title()
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
        elif tup[0] == 'torah':
            description = f'{title}<br /><br />This {item.segment_title} class on Parashat {item.unit_title} is taught by {teacher}.'
            if item.section_sponsor:
                description = f'{description}<br /><br />Sefer {item.section_title}<br />{item.section_sponsor}'
            else:
                description = f'{description}<br /><br />Sefer {item.section_title}<br /><i>Sponsorship available</i>'
            if item.unit_sponsor:
                description = f'{description}<br /><br />Parashat {item.unit_title}<br />{item.unit_sponsor}'
            else:
                description = f'{description}<br /><br />Parashat {item.unit_title}<br /><i>Sponsorship available</i>'
        elif tup[0] == 'parasha':
            description = f'{title}<br /><br />This part in Parashat {item.unit_title} is taught by {teacher}.'
            if item.section_sponsor:
                description = f'{description}<br /><br />Sefer {item.section_title}<br />{item.section_sponsor}'
            else:
                description = f'{description}<br /><br />Sefer {item.section_title}<br /><i>Sponsorship available</i>'
            if item.unit_sponsor:
                description = f'{description}<br /><br />Parashat {item.unit_title}<br />{item.unit_sponsor}'
            else:
                description = f'{description}<br /><br />Parashat {item.unit_title}<br /><i>Sponsorship available</i>'
        elif tup[0] == 'neviim_rishonim' or tup[0] == 'neviim_aharonim' or tup[0] == 'tere_assar' or tup[0] == 'ketuvim':
            description = f'{title}<br /><br />This perek in Sefer {item.section_title} is taught by {teacher}.'
            if item.section_sponsor:
                description = f'{description}<br /><br />Sefer {item.section_title}<br />{item.section_sponsor}'
            else:
                description = f'{description}<br /><br />Sefer {item.section_title}<br /><i>Sponsorship available</i>'
            if item.unit_sponsor:
                description = f'{description}<br /><br />Perek {item.unit}<br />{item.unit_sponsor}'
        elif tup[0] == 'mishna':
            description = f'{title}<br /><br />This mishna in Masechet {item.section_title} is taught by {teacher}.'
            description = f'{description}<br /><br />In Loving Memory of Mr. Ovadia Buddy Sutton A"H<br />'
            if item.segment_sponsor:
                description = f'{description}<br /><br />Seder {item.segment_title}<br />{item.segment_sponsor}'
            else:
                description = f'{description}<br /><br />Seder {item.segment_title}<br /><i>Sponsorship available</i>'
            if item.section_sponsor:
                description = f'{description}<br /><br />Masechet {item.section_title}<br />{item.section_sponsor}'
            else:
                description = f'{description}<br /><br />Masechet {item.section_title}<br /><i>Sponsorship available</i>'
            if item.unit_sponsor:
                description = f'{description}<br /><br />Perek {item.unit}<br />{item.unit_sponsor}'
            else:
                description = f'{description}<br /><br />Perek {item.unit}<br /><i>Sponsorship available</i>'
        else:
            raise Exception(f'unsupported division {tup[0]}')

        return f'{description}<br /><br /><audio controls=""><source src="https://cdn.tanachstudy.com/{item.audio}"></audio>'

    def item_link(self, tup):
        host = 'https://tanachstudy.com'
        return f'{host}{tup[1].get_location()}'

    def item_enclosure_url(self, item):
        return f'https://cdn.tanachstudy.com/{item[1].audio}'

    def image(self, item):
        return 'https://cdn.tanachstudy.com/assets/images/mishna-study-logo.png'

    item_enclosure_mime_type = 'audio/mpeg'


class AtomAllFeed(RSSAllFeed):
    feed_type = Atom1Feed
    subtitle = RSSAllFeed.description
    link = "/feeds/atom/all"
