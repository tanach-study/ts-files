from django.db import models


class Teacher(models.Model):
    title = models.CharField(max_length=20)
    fname = models.CharField(max_length=40)
    mname = models.CharField(max_length=10, default=None, null=True, blank=True)
    lname = models.CharField(max_length=40)
    short_bio = models.CharField(max_length=256)
    long_bio = models.TextField()
    image_url = models.CharField(max_length=1024, null=True, blank=True)
    image = models.FileField(upload_to='uploads/', null=True, blank=True)

    def __str__(self):
        if not self.mname:
            return '{} {} {} {}'.format(self.title, self.fname, self.mname, self.lname)
        return '{} {} {}'.format(self.title, self.fname, self.lname)


class Class(models.Model):
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
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_DEFAULT, default=None, null=True)
    date = models.DateTimeField(null=True, blank=True)
    video_url = models.CharField(max_length=1024)

    def __str__(self):
        segment = self.segment_title
        section = self.section.title()
        unit = self.unit.title()
        if self.division == 'parasha' or self.division == 'mishna':
            return '{} - {}: {} {} {}'.format(self.division_title, self.segment_title, section, unit, self.part)
        if not self.part:
            return '{} - Sefer {}: Perek {}'.format(self.division_title, section, unit)
        return '{} - Sefer {}: Perek {} Part {}'.format(self.division_title, section, unit, self.part)


class Teamim(models.Model):
    reader = models.ForeignKey(Teacher, on_delete=models.SET_DEFAULT, default=None, null=True)
    audio = models.FileField(upload_to='uploads/', null=True, blank=True)
    post = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)
