from django.db import models


class Teacher(models.Model):
    title = models.TextField()
    fname = models.TextField()
    mname = models.TextField()
    lname = models.TextField()
    short_bio = models.TextField()
    long_bio = models.TextField()
    image_url = models.TextField()


class Teamim(models.Model):
    reader = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    audio_url = models.TextField()


class Classes(models.Model):
    division = models.CharField(max_length=256)
    division_name = models.CharField(max_length=256)
    division_title = models.CharField(max_length=256)
    division_sponsor = models.CharField(max_length=256)
    division_sequence = models.CharField(max_length=256)
    segment = models.CharField(max_length=256)
    segment_name = models.CharField(max_length=256)
    segment_title = models.CharField(max_length=256)
    segment_sponsor = models.CharField(max_length=256)
    segment_sequence = models.CharField(max_length=256)
    section = models.CharField(max_length=256)
    section_name = models.CharField(max_length=256)
    section_title = models.CharField(max_length=256)
    section_sponsor = models.CharField(max_length=256)
    section_sequence = models.CharField(max_length=256)
    unit = models.CharField(max_length=256)
    unit_name = models.CharField(max_length=256)
    unit_title = models.CharField(max_length=256)
    unit_sponsor = models.CharField(max_length=256)
    unit_sequence = models.CharField(max_length=256)
    part = models.CharField(max_length=256)
    part_name = models.CharField(max_length=256)
    part_title = models.CharField(max_length=256)
    part_sponsor = models.CharField(max_length=256)
    part_sequence = models.CharField(max_length=256)
    series = models.CharField(max_length=256)
    series_name = models.CharField(max_length=256)
    series_title = models.CharField(max_length=256)
    series_sponsor = models.CharField(max_length=256)
    series_sequence = models.CharField(max_length=256)
    start_chapter = models.CharField(max_length=256)
    start_verse = models.CharField(max_length=256)
    end_chapter = models.CharField(max_length=256)
    end_verse = models.CharField(max_length=256)
    audio_url = models.CharField(max_length=1024)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    teamim = models.ForeignKey(Teamim, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True)
    video_url = models.CharField(max_length=1024)

    def __str__(self):
        return '{} {} {} {} {}'.format(self.division, self.segment, self.section, self.unit, self.part)
