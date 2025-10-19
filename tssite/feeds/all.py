import datetime

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from tssite.models import Class, TalmudStudy


class RSSAllFeed(Feed):
    title = "Tanach Study Daily Updates"
    link = "/feeds/rss/all"
    description = "Description of Tanach Study Daily Updates"

    def items(self):
        items = []
        for torah in Class.objects.exclude(date__isnull=True).filter(
            division_sequence=1, date__lte=datetime.datetime.now()
        )[:500]:
            items.append((torah.division, torah))

        for parasha in Class.objects.exclude(date__isnull=True).filter(
            division_sequence=7, date__lte=datetime.datetime.now()
        )[:500]:
            items.append((parasha.division, parasha))

        for neviim_rishonim in Class.objects.exclude(date__isnull=True).filter(
            division_sequence=2, date__lte=datetime.datetime.now()
        )[:500]:
            items.append((neviim_rishonim.division, neviim_rishonim))

        for neviim_aharonim in Class.objects.exclude(date__isnull=True).filter(
            division_sequence=3, date__lte=datetime.datetime.now()
        )[:500]:
            items.append((neviim_aharonim.division, neviim_aharonim))

        for tere_assar in Class.objects.exclude(date__isnull=True).filter(
            division_sequence=4, date__lte=datetime.datetime.now()
        )[:500]:
            items.append((tere_assar.division, tere_assar))

        for ketuvim in Class.objects.exclude(date__isnull=True).filter(
            division_sequence=5, date__lte=datetime.datetime.now()
        )[:500]:
            items.append((ketuvim.division, ketuvim))

        for mishna in Class.objects.exclude(date__isnull=True).filter(
            division_sequence=6, date__lte=datetime.datetime.now()
        )[:500]:
            items.append((mishna.division, mishna))

        for i in TalmudStudy.objects.all().order_by("-date", "-teacher")[:500]:
            items.append(("talmud", i))
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
        # title = str(item)
        # teacher = str(item.teacher)
        class_title = ""
        if tup[0] == "talmud":
            seder = item.seder.title()
            masechet = item.masechet.title()
            # link = item.get_location()
            seder_sponsor = "" if not item.seder_sponsor else item.seder_sponsor
            masechet_sponsor = (
                "" if not item.masechet_sponsor else item.masechet_sponsor
            )
            daf_sponsor = "" if not item.daf_sponsor else item.daf_sponsor
            description = f"Seder {seder}"

            if seder_sponsor:
                description = f"{description}<br />{seder_sponsor}"
            description = f"{description}<br />Masechet {masechet}"

            if masechet_sponsor:
                description = f"{description}<br />{masechet_sponsor}"

            description = f"{description}<br />Daf {item.daf}"
            if daf_sponsor:
                description = f"{description}<br />{daf_sponsor}"

        elif tup[0] == "parasha":
            description = f"Sefer {item.section_title}"
            if item.section_sponsor:
                description = f"{description}<br />{item.section_sponsor}"

            description = f"{description}<br />Parashat {item.unit_title}"
            if item.unit_sponsor:
                description = f"{description}<br />{item.unit_sponsor}"

        elif tup[0] == "torah":
            class_title = item.part_title
            description = f"Sefer {item.section_title}"
            if item.section_sponsor:
                description = f"{description}<br />{item.section_sponsor}"

            description = f"{description}<br />Parashat {item.unit_title}"
            if item.unit_sponsor:
                description = f"{description}<br />{item.unit_sponsor}"

        elif (
            tup[0] == "neviim_rishonim"
            or tup[0] == "neviim_aharonim"
            or tup[0] == "tere_assar"
            or tup[0] == "ketuvim"
        ):
            class_title = item.unit_title
            description = f"Sefer {item.section_title}"
            if item.section_sponsor:
                description = f"{description}<br />{item.section_sponsor}"

            description = f"{description}<br />Perek {item.unit}"
            if item.unit_sponsor:
                description = f"{description}<br />{item.unit_sponsor}"

        elif tup[0] == "mishna":
            class_title = item.part_title
            description = 'In Loving Memory of Mr. Ovadia Buddy Sutton A"H<br />'
            description = f"{description}<br />Seder {item.segment_title}"
            if item.segment_sponsor:
                description = f"{description}<br />{item.segment_sponsor}"

            description = f"{description}<br />Masechet {item.section_title}"
            if item.section_sponsor:
                description = f"{description}<br />{item.section_sponsor}"

            description = f"{description}<br />Perek {item.unit}"
            if item.unit_sponsor:
                description = f"{description}<br />{item.unit_sponsor}"

        else:
            raise Exception(f"unsupported division {tup[0]}")

        if class_title != "":
            return f'<b>{class_title}</b><br />{description}<br /><audio controls=""><source src="https://cdn.tanachstudy.com/{item.audio}"></audio>'
        return f'{description}<br /><audio controls=""><source src="https://cdn.tanachstudy.com/{item.audio}"></audio>'

    def item_link(self, tup):
        host = "https://tanachstudy.com"
        return f"{host}{tup[1].get_location()}"

    def item_enclosure_url(self, item):
        return f"https://cdn.tanachstudy.com/{item[1].audio}"

    item_enclosure_mime_type = "audio/mpeg"


class AtomAllFeed(RSSAllFeed):
    feed_type = Atom1Feed
    subtitle = RSSAllFeed.description
    link = "/feeds/atom/all"
