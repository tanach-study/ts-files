from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Class, Teacher, Teamim


def index(request):
    return HttpResponse("<a href='/admin'>Click here for admin page</a>")


def all(request):
    values = []
    all_classes = Class.objects.all()
    for c in all_classes:
        teamim = None
        if len(c.teamim_set.all()) > 0:
            teamim = []
            for t in c.teamim_set.all():
                teamim.append({
                    'reader_title': t.reader.title if t.reader.title is not '' else None,
                    'reader_fname': t.reader.fname if t.reader.fname is not '' else None,
                    'reader_mname': t.reader.mname if t.reader.mname is not '' else None,
                    'reader_lname': t.reader.lname if t.reader.lname is not '' else None,
                    'audio_url': t.audio.url,
                })
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
            'teamim': teamim,
            'teacher_title': c.teacher.title,
            'teacher_fname': c.teacher.fname,
            'teacher_mname': c.teacher.mname,
            'teacher_lname': c.teacher.lname,
            'teacher_short_bio': c.teacher.short_bio,
            'teacher_long_bio': c.teacher.long_bio,
            'teacher_image_url': c.teacher.image_url,
            'date': c.date,
            'video_url': c.video_url,
          })
    values = [{k: v for k, v in obj.items() if v is not None} for obj in values]
    return JsonResponse(values, safe=False)
