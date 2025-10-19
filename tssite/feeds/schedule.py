import datetime

from django.contrib.syndication.views import Feed

from tssite.models import Schedule


class ScheduleFeed(Feed):
    def get_object(self, request, schedule_id):
        s = Schedule.objects.get(id=schedule_id)
        print('in get_object; schedule_id:', schedule_id, 's:', s)
        return s

    def title(self, obj):
        return f'Tanach Study: {obj.name}'

    def link(self, obj):
        return f'feeds/rss/schedules/{obj.id}'

    def description(self, obj):
        return f'Tanach Study generated feed for the schedule {obj.name}. Tanach Study is an initiative to promote the independent study of the books of Tanach (Torah, Neviim and Ketuvim). Tanach Study hopes to broaden Torah learning, to increase knowledge of our Jewish history, heighten our Yirat Shamayim, Ahavat Hashem, and strengthen our personal as well as our national identity.'

    def items(self, obj):
        return obj.get_classes()

    def item_title(self, tup):
        return str(tup[1])

    def item_pubdate(self, tup):
        return datetime.datetime(tup[0].year, tup[0].month, tup[0].day)

    def item_author_name(self, tup):
        return tup[1].teacher.__str__()

    def item_description(self, tup):
        description = ''
        item = tup[1]
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
            raise Exception(f'unsupported division {tup[0]}')

        if class_title != '':
            return f'<b>{class_title}</b><br />{description}<br /><audio controls=""><source src="https://cdn.tanachstudy.com/{item.audio}"></audio>'
        return f'{description}<br /><audio controls=""><source src="https://cdn.tanachstudy.com/{item.audio}"></audio>'

    def item_link(self, tup):
        host = 'https://tanachstudy.com'
        return f'{host}{tup[1].get_location()}'

    def item_enclosure_url(self, item):
        return f'https://cdn.tanachstudy.com/{item[1].audio}'

    item_enclosure_mime_type = 'audio/mpeg'
