import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Class, Teacher, Teamim, TalmudSponsor, TalmudStudy, Schedule
from collections import defaultdict
from hdate import HDate

def index(request):
    return HttpResponse("<a href='/admin'>Click here for admin page</a>")


def all(request):
    values = []

    teachers_map = {}
    for t in Teacher.objects.all():
        teachers_map[t.id] = t

    teamim_map = defaultdict(list)
    for t in Teamim.objects.all():
        teamim_map[t.post_id].append(t)

    all_classes = Class.objects.all()
    for c in all_classes:
        teamim = []
        for t in teamim_map[c.id]:
            this_reader = teachers_map[t.reader_id]
            teamim.append({
                'reader_title': this_reader.title if this_reader.title is not '' else None,
                'reader_fname': this_reader.fname if this_reader.fname is not '' else None,
                'reader_mname': this_reader.mname if this_reader.mname is not '' else None,
                'reader_lname': this_reader.lname if this_reader.lname is not '' else None,
                'audio_url': t.audio.url,
            })
        this_teacher = teachers_map[c.teacher_id]
        values.append({
            'division': c.division if c.division is not '' else None,
            'division_name': c.division_name if c.division_name is not '' else None,
            'division_title': c.division_title if c.division_title is not '' else None,
            'division_sponsor': c.division_sponsor if c.division_sponsor is not '' else None,
            'division_sequence': c.division_sequence if c.division_sequence is not '' else None,
            'segment': c.segment if c.segment is not '' else None,
            'segment_name': c.segment_name if c.segment_name is not '' else None,
            'segment_title': c.segment_title if c.segment_title is not '' else None,
            'segment_sponsor': c.segment_sponsor if c.segment_sponsor is not '' else None,
            'segment_sequence': c.segment_sequence if c.segment_sequence is not '' else None,
            'section': c.section if c.section is not '' else None,
            'section_name': c.section_name if c.section_name is not '' else None,
            'section_title': c.section_title if c.section_title is not '' else None,
            'section_sponsor': c.section_sponsor if c.section_sponsor is not '' else None,
            'section_sequence': c.section_sequence if c.section_sequence is not '' else None,
            'unit': c.unit if c.unit is not '' else None,
            'unit_name': c.unit_name if c.unit_name is not '' else None,
            'unit_title': c.unit_title if c.unit_title is not '' else None,
            'unit_sponsor': c.unit_sponsor if c.unit_sponsor is not '' else None,
            'unit_sequence': c.unit_sequence if c.unit_sequence is not '' else None,
            'part': c.part if c.part is not '' else None,
            'part_name': c.part_name if c.part_name is not '' else None,
            'part_title': c.part_title if c.part_title is not '' else None,
            'part_sponsor': c.part_sponsor if c.part_sponsor is not '' else None,
            'part_sequence': c.part_sequence if c.part_sequence is not '' else None,
            'series': c.series if c.series is not '' else None,
            'series_name': c.series_name if c.series_name is not '' else None,
            'series_title': c.series_title if c.series_title is not '' else None,
            'series_sponsor': c.series_sponsor if c.series_sponsor is not '' else None,
            'series_sequence': c.series_sequence if c.series_sequence is not '' else None,
            'start_chapter': c.start_chapter if c.start_chapter is not '' else None,
            'start_verse': c.start_verse if c.start_verse is not '' else None,
            'end_chapter': c.end_chapter if c.end_chapter is not '' else None,
            'end_verse': c.end_verse if c.end_verse is not '' else None,
            'audio_url': c.audio_url if c.audio_url is not '' else None,
            'audio': c.audio.url if c.audio else '',
            'teamim': teamim if teamim else None,
            'teacher_title': this_teacher.title,
            'teacher_fname': this_teacher.fname,
            'teacher_mname': this_teacher.mname,
            'teacher_lname': this_teacher.lname,
            'teacher_short_bio': this_teacher.short_bio,
            'teacher_long_bio': this_teacher.long_bio,
            'teacher_image_url': this_teacher.image_url,
            'date': c.date,
            'video_url': c.video_url,
          })

    talmud_sponsors_map = {}
    for s in TalmudSponsor.objects.all():
        talmud_sponsors_map[s.id] = str(s)

    talmud_classes = TalmudStudy.objects.all()
    for c in talmud_classes:
        this_teacher = teachers_map[c.teacher_id]
        values.append({
            'division': 'talmud',
            'division_name': None,
            'division_title': 'Talmud',
            'division_sponsor': None,
            'division_sequence': 7,
            'segment': c.seder,
            'segment_name': 'Seder',
            'segment_title': c.seder.title(),
            'segment_sponsor': None if not c.seder_sponsor else talmud_sponsors_map[c.seder_sponsor],
            'segment_sequence': None if not c.seder_sequence else c.seder_sequence,
            'section': c.masechet,
            'section_name': 'Masechet',
            'section_title': c.masechet.title(),
            'section_sponsor': None if not c.masechet_sponsor else talmud_sponsors_map[c.masechet_sponsor],
            'section_sequence': None if not c.masechet_sequence else c.masechet_sequence,
            'unit': c.daf,
            'unit_name': 'Daf',
            'unit_title': c.daf,
            'unit_sponsor': None if not c.daf_sponsor else talmud_sponsors_map[c.daf_sponsor],
            'unit_sequence': c.daf,
            'part': '',
            'part_name': '',
            'part_title': '',
            'part_sponsor': '',
            'part_sequence': '',
            'series': 'first',
            'series_name': '',
            'series_title': '',
            'series_sponsor': '',
            'series_sequence': '',
            'audio': c.audio.url if c.audio else '',
            'teamim': '',
            'teacher_title': this_teacher.title,
            'teacher_fname': this_teacher.fname,
            'teacher_mname': this_teacher.mname,
            'teacher_lname': this_teacher.lname,
            'teacher_short_bio': this_teacher.short_bio,
            'teacher_long_bio': this_teacher.long_bio,
            'teacher_image_url': this_teacher.image_url,
            'date': c.date,
          })
    values = [{k: v for k, v in obj.items() if v is not None} for obj in values]
    return JsonResponse(values, safe=False)


def schedules(request):
    html = '<h1>Schedules</h1>\n<ul>\n'
    for s in Schedule.objects.all():
        html += f'<li><a href="/schedule/{s.id}">{s.name}</a></li>\n'
    html += '</ul>\n'
    return HttpResponse(html)

def schedule(request, schedule_id):
    s = Schedule.objects.filter(id=schedule_id).get()
    start_date = s.start_date
    today = datetime.date.today()
    diff = today - start_date
    print(type(start_date), start_date, diff.days)

    classes = Class.objects
    # show perakim starting with neviim rishonim (division=2)...
    classes = classes.filter(division_sequence__gte=2)
    # ...through ketuvim (division=5), inclusive
    classes = classes.filter(division_sequence__lte=5)
    # TODO(joey): only show one class if the perek has multiple parts
    # classes = classes.filter(part='')
    # introductions should be counted on the same day as chapter 1
    classes = classes.exclude(unit='0')
    # only get the number of classes between the start date and today
    classes = classes[:diff.days]

    html = f'<h1>Items for Schedule: {s}</h1>\n<ul>\n'
    date_iterator = 0
    class_iterator = 0
    curr_date = start_date + datetime.timedelta(days=date_iterator)

    schedule_pauses = s.schedulepause_set.all()
    print("schedule_pauses:", schedule_pauses)
    while curr_date <= today and class_iterator < len(classes):
        print("curr_date:", curr_date, "date_iterator:", date_iterator, "class_iterator:", class_iterator)
        # get the next date to display

        # skip any date in a SchedulePause
        for pause in schedule_pauses:
            if pause.start_date == curr_date:
                pause_dur = pause.end_date - pause.start_date
                skipped_days = pause_dur.days
                if skipped_days == 0:
                    skipped_days = 1
                date_iterator += skipped_days
                print(f'skipping {skipped_days} days due to pause: {pause}')
                curr_date = start_date + datetime.timedelta(days=date_iterator)

        # always skip saturdays and yom tov
        hebrew_date = HDate(curr_date, diaspora=True)
        if curr_date.weekday() == 5 or hebrew_date.is_yom_tov: # Monday = 0; Sunday = 6
            date_iterator += 1
            curr_date = start_date + datetime.timedelta(days=date_iterator)
            continue

        # output the class with the date
        c = classes[class_iterator]
        html += f'<li>Date: {curr_date}; Class: {c}</li>\n'

        date_iterator += 1
        class_iterator += 1
        curr_date = start_date + datetime.timedelta(days=date_iterator)

    html += '</ul>\n'
    return HttpResponse(html)
