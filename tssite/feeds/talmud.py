from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from tssite.models import TalmudStudy


class RSSTalmudFeed(Feed):
    title = "Talmud Study"
    link = "/feeds/rss/talmud-study"
    description = "Talmud Study is an initiative to promote the independent study of the Talmud Bavli through a web-based platform and weekly class. Our program aims to provide the Jewish community with immediate access to Torah knowledge in the form of a daily e-mail/podcast to complete and understand the Talmud with the Daf Yomi cycle. Talmud Study hopes to broaden Torah learning, to increase knowledge of our Jewish history, heighten our Yirat Shamayim, Ahavat Hashem, and strengthen our personal as well as our national identity."

    item_author_name = "Talmud Study"
    item_author_email = "info@tanachstudy.com"

    def items(self):
        return TalmudStudy.objects.all().order_by("-date", "-teacher")[:500]

    def item_title(self, item):
        return str(item)

    def item_description(self, item):
        title = str(item)
        seder = item.seder.title()
        masechet = item.masechet.title()
        teacher = str(item.teacher)
        # link = item.get_location()
        seder_sponsor = "" if not item.seder_sponsor else item.seder_sponsor
        masechet_sponsor = "" if not item.masechet_sponsor else item.masechet_sponsor
        daf_sponsor = "" if not item.daf_sponsor else item.daf_sponsor

        description = f"{title}<br /><br />This daf in {seder} is taught by {teacher}."
        if seder_sponsor:
            description = f"{description}<br /><br />Seder {seder}<br />{seder_sponsor}"
        else:
            description = f"{description}<br /><br />Seder {seder}<br /><i>Sponsorship available</i>"
        if masechet_sponsor:
            description = (
                f"{description}<br /><br />Masechet {masechet}<br />{masechet_sponsor}"
            )
        else:
            description = f"{description}<br /><br />Masechet {masechet}<br /><i>Sponsorship available</i>"
        if daf_sponsor:
            description = f"{description}<br /><br />Daf {item.daf}<br />{daf_sponsor}"
        else:
            description = f"{description}<br /><br />Daf {item.daf}<br /><i>Sponsorship available</i>"
        return description

    def item_link(self, item):
        host = "https://tanachstudy.com"
        return f"{host}{item.get_location()}"

    def item_enclosure_url(self, item):
        return f"https://cdn.tanachstudy.com/{item.audio}"

    item_enclosure_mime_type = "audio/mpeg"


class AtomTalmudFeed(RSSTalmudFeed):
    feed_type = Atom1Feed
    subtitle = RSSTalmudFeed.description
    link = "/feeds/atom/talmud-study"
