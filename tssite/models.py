import uuid
from django.db import models
from .validators import validate_file_extension
from django.conf import settings
from tssite import client

masechetot_by_seder = [
    ('Zeraim', (
            ('berachot', 'Berachot'),
        )
    ),
    ('Moed', (
            ('shabbat', 'Shabbat'),
        )
    ),
]

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
        if self.mname:
            return '{} {} {} {}'.format(self.title, self.fname, self.mname, self.lname)
        return '{} {} {}'.format(self.title, self.fname, self.lname)

    @property
    def teacher_string(self):
        string = ''
        if self.mname:
            title = self.title.replace('.', '').lower()
            first = self.fname.lower()
            middle = self.mname.replace('.', '').lower()
            last = self.lname.lower()
            string = f'{title}-{first}-{middle}-{last}'
        else:
            title = self.title.replace('.', '').lower()
            first = self.fname.lower()
            last = self.lname.lower()
            string = f'{title}-{first}-{last}'
        return string



def get_class_audio_location(instance, filename):
    path = ''
    if instance.division == 'torah':
        path = f'archives/Torah/{instance.section_title}/{instance.unit}-{instance.part}.mp3'
    elif (
        instance.division == 'neviim_rishonim' or
        instance.division == 'neviim_aharonim' or
        instance.division == 'tere_assar'
    ):
        base = ''
        if instance.division == 'neviim_rishonim':
            base = 'archives/Neviim Rishonim'
        elif instance.division == 'neviim_aharonim':
            base = 'archives/Neviim Aharonim'
        elif instance.division == 'tere_assar':
            base = 'archives/Tere Asar'

        file = ''
        if instance.part is not None and instance.part is not '':
            file = f'{instance.section}-{instance.unit}{instance.part}'
        else:
            file = f'{instance.section}-{instance.unit}'
        path = f'{base}/{instance.section.title()}/{file}.mp3'

    elif instance.division == 'ketuvim':
        base = 'archives/Ketuvim'
        file = ''
        if instance.part is not None and instance.part is not '':
            file = f'{instance.section}-{instance.unit}{instance.part}'
        else:
            file = f'{instance.section}-{instance.unit}'
        path = f"{base}/{instance.section_title}/{file}.mp3"

    elif instance.division == 'parasha':
        base = 'archives/parasha'
        common = f'{base}/{instance.segment}/{instance.segment}-{instance.section}-{instance.unit}'
        if instance.series is not None and instance.series is not 'first':
            path = f'{common}-{instance.series}-{instance.teacher.teacher_string}.mp3'
        else:
            path = f'{common}-{instance.teacher.teacher_string}.mp3'

    elif instance.division == 'mishna':
        base = 'archives/mishna'
        file = f'{instance.segment}-{instance.section}-{instance.unit}-{instance.part}-{instance.teacher.teacher_string}'
        path = f'{base}/{instance.segment}/{instance.section}/{file}.mp3'

    else:
        raise Exception(f'division is invalid: {instance.division}')

    return path

def create_transcoder_job(audio_field):
    if client is None:
        raise Exception('client not initialized')

    s3_key = str(audio_field)

    client.create_job(
        PipelineId=settings.AWS_TRANSCODER_PIPELINE_ID,
        Input={
            'Key': s3_key,
        },
        Output={
            'Key': s3_key,
            'PresetId': settings.AWS_TRANSCODER_PRESET_ID,
        }
    )
    print('created transcoder job')

class Class(models.Model):
    division = models.CharField(max_length=256)
    division_name = models.CharField(max_length=256, null=True, blank=True)
    division_title = models.CharField(max_length=256, null=True, blank=True)
    division_sponsor = models.CharField(max_length=256, null=True, blank=True)
    division_sequence = models.IntegerField(null=True, blank=True)
    segment = models.CharField(max_length=256, null=True, blank=True)
    segment_name = models.CharField(max_length=256, null=True, blank=True)
    segment_title = models.CharField(max_length=256, null=True, blank=True)
    segment_sponsor = models.CharField(max_length=256, null=True, blank=True)
    segment_sequence = models.IntegerField(null=True, blank=True)
    section = models.CharField(max_length=256)
    section_name = models.CharField(max_length=256, null=True, blank=True)
    section_title = models.CharField(max_length=256, null=True, blank=True)
    section_sponsor = models.CharField(max_length=256, null=True, blank=True)
    section_sequence = models.IntegerField(null=True, blank=True)
    unit = models.CharField(max_length=256)
    unit_name = models.CharField(max_length=256, null=True, blank=True)
    unit_title = models.CharField(max_length=256, null=True, blank=True)
    unit_sponsor = models.CharField(max_length=256, null=True, blank=True)
    unit_sequence = models.IntegerField(null=True, blank=True)
    part = models.CharField(max_length=256, null=True, blank=True)
    part_name = models.CharField(max_length=256, null=True, blank=True)
    part_title = models.CharField(max_length=256, null=True, blank=True)
    part_sponsor = models.CharField(max_length=256, null=True, blank=True)
    part_sequence = models.IntegerField(null=True, blank=True)
    series = models.CharField(max_length=256, null=True, blank=True)
    series_name = models.CharField(max_length=256, null=True, blank=True)
    series_title = models.CharField(max_length=256, null=True, blank=True)
    series_sponsor = models.CharField(max_length=256, null=True, blank=True)
    series_sequence = models.IntegerField(null=True, blank=True)
    start_chapter = models.CharField(max_length=256, null=True, blank=True)
    start_verse = models.CharField(max_length=256, null=True, blank=True)
    end_chapter = models.CharField(max_length=256, null=True, blank=True)
    end_verse = models.CharField(max_length=256, null=True, blank=True)
    audio_url = models.CharField(max_length=1024, null=True, blank=True)
    audio = models.FileField(upload_to=get_class_audio_location, validators=[validate_file_extension], default=None, null=True, max_length=500)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_DEFAULT, default=None, null=True)
    date = models.DateTimeField(null=True, blank=True)
    video_url = models.CharField(max_length=1024, null=True, blank=True)

    class Meta:
        ordering = ['series_sequence', 'division_sequence', 'segment_sequence', 'section_sequence', 'unit_sequence', 'part_sequence', 'series_sequence', '-date']


    def get_location(self):
        toreturn = ''

        if self.division == 'torah':
            toreturn = f'/parasha-study/perakim/{self.section}/{self.unit}?part={self.part}'
        elif (
            self.division == 'neviim_rishonim' or
            self.division == 'neviim_aharonim' or
            self.division == 'tere_assar' or
            self.division == 'ketuvim'
        ):
            if self.part:
                toreturn = f'/tanach-study/perakim/{self.section}/{self.unit}?part={self.part}'
            else:
                toreturn = f'/tanach-study/perakim/{self.section}/{self.unit}'

        elif self.division == 'parasha':
            toreturn = f'/parasha-plus-study/sefarim/{self.segment}/{self.section}?part={self.unit}'

        elif self.division == 'mishna':
            toreturn = f'/mishna-study/perek/{self.segment}/{self.section}/{self.unit}?part={self.part}'
        return toreturn


    def __str__(self):
        audio = get_class_audio_location(self, '')
        toreturn = ''

        if self.division == 'torah':
            toreturn = f'Torah - Sefer {self.section_title} Parashat {self.unit_title}: Part {self.part}'
        elif (
            self.division == 'neviim_rishonim' or
            self.division == 'neviim_aharonim' or
            self.division == 'tere_assar' or
            self.division == 'ketuvim'
        ):
            if self.part:
                toreturn = f'Tanach - Sefer {self.section_title}: Perek {self.unit.title()} Part {self.part}'
            else:
                toreturn = f'Tanach - Sefer {self.section_title}: Perek {self.unit.title()}'

        elif self.division == 'parasha':
            if self.series is not None:
                toreturn = f'{self.division.title()} - {self.segment_title}: {self.section_title} {self.unit.title()} ({self.series.title()})'
            else:
                toreturn = f'{self.division.title()} - {self.segment_title}: {self.section_title} {self.unit.title()}'

        elif self.division == 'mishna':
            toreturn = f'{self.division_title} - {self.segment_title}: {self.section_title} Perek {self.unit.title()} Mishna {self.part}'
        return toreturn


def get_teamim_audio_location(instance, filename):
    path = ''
    reader_string = instance.reader.teacher_string
    if instance.post.division == 'torah':
        path = f'archives/Torah/{instance.post.section_title}/recordings/{reader_string}-{instance.post.unit}-{instance.post.part}-teamim.mp3'
    elif (
        instance.post.division == 'neviim_rishonim' or
        instance.post.division == 'neviim_aharonim' or
        instance.post.division == 'tere_assar'
    ):
        base = ''
        if instance.post.division == 'neviim_rishonim':
            base = 'archives/Neviim Rishonim'
        elif instance.post.division == 'neviim_aharonim':
            base = 'archives/Neviim Aharonim'
        elif instance.post.division == 'tere_assar':
            base = 'archives/Tere Asar'

        file = ''
        if instance.post.part is not None and instance.post.part is not '':
            file = f'{instance.post.section}-{instance.post.unit}{instance.post.part}'
        else:
            file = f'{instance.post.section}-{instance.post.unit}'
        path = f'{base}/{instance.post.section.title()}/recordings/{reader_string}-{file}-teamim.mp3'

    elif instance.post.division == 'ketuvim':
        base = 'archives/Ketuvim'
        file = ''
        if instance.post.part is not None and instance.post.part is not '':
            file = f'{instance.post.section}-{instance.post.unit}{instance.post.part}'
        else:
            file = f'{instance.post.section}-{instance.post.unit}'
        path = f"{base}/{instance.post.section_title}/recordings/{reader_string}-{file}-teamim.mp3"

    elif instance.post.division == 'parasha':
        base = 'archives/parasha'
        path = f'{base}/{instance.post.segment}/recordings/{reader_string}-{instance.post.segment}-{instance.post.section}-{instance.post.unit}-teamim.mp3'

    elif instance.post.division == 'mishna':
        base = 'archives/mishna'
        # TODO(joey): remove teacher_string, add reader_string
        file = f'{instance.post.segment}-{instance.post.section}-{instance.post.unit}-{instance.post.part}-{instance.post.teacher.teacher_string}'
        path = f'{base}/{instance.post.segment}/{instance.post.section}/recordings/{file}-teamim.mp3'

    else:
        raise Exception(f'division is invalid: {instance.post.division}')

    return path


class Teamim(models.Model):
    reader = models.ForeignKey(Teacher, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True)
    audio = models.FileField(upload_to=get_teamim_audio_location, default=None, null=True, blank=True, max_length=500)
    post = models.ForeignKey(Class, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True)

    def __str__(self):
        return f'{self.post} Read By {self.reader}'


class ShasSedarim(models.TextChoices):
    ZERAIM = 'zeraim', 'Zeraim'
    MOED = 'moed', 'Moed'
    NASHIM = 'nashim', 'Nashim'
    NEZIKIN = 'nezikin', 'Nezikin'
    KADASHIM = 'kadashim', 'Kadashim'
    TAHAROT = 'taharot', 'Taharot'


class TalmudSponsor(models.Model):
    line_one = models.CharField(max_length=1024)
    line_two = models.CharField(max_length=1024, blank=True, null=True)
    line_three = models.CharField(max_length=1024, blank=True, null=True)

    def __str__(self):
        s = ''
        if self.line_one:
            s = s + ' ' + self.line_one
        if self.line_two:
            s = s + ' ' + self.line_two
        if self.line_three:
            s = s + ' ' + self.line_three
        return s


def get_talmud_audio_location(instance, filename):
    base = 'archives/talmud'
    file = f'{instance.seder}-{instance.masechet}-{instance.daf}-{instance.teacher.teacher_string}'
    path = f'{base}/{instance.seder}/{instance.masechet}/{file}.mp3'
    return path


class TalmudStudy(models.Model):
    MASECHET_CHOICES = masechetot_by_seder

    seder = models.CharField(max_length=12, choices=ShasSedarim.choices)
    seder_sponsor = models.ForeignKey(TalmudSponsor, related_name='+', on_delete=models.SET_DEFAULT, default=None, null=True, blank=True)
    seder_sequence = models.IntegerField(null=True, blank=True)
    masechet = models.CharField(max_length=50, choices=MASECHET_CHOICES)
    masechet_sponsor = models.ForeignKey(TalmudSponsor, related_name='+', on_delete=models.SET_DEFAULT, default=None, null=True, blank=True)
    masechet_sequence = models.IntegerField(null=True, blank=True)
    daf = models.IntegerField()
    daf_sponsor = models.ForeignKey(TalmudSponsor, related_name='+', on_delete=models.SET_DEFAULT, default=None, null=True, blank=True)

    audio = models.FileField(upload_to=get_talmud_audio_location, validators=[validate_file_extension], default=None, null=True, max_length=500)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_DEFAULT, default=None, null=True)
    date = models.DateTimeField()

    models.UniqueConstraint(fields=['masechet', 'daf', 'amud'], name='unique_daf_amud_per_masechet')

    def __str__(self):
        return f'Masechet {self.masechet.title()} Daf {self.daf} with {str(self.teacher)}'

    def get_location(self):
        teacher = str(self.teacher).lower().replace('.', '').replace(' ', '-')
        return f'/talmud-study/dapim/{self.seder}/{self.masechet}/{self.daf}?{teacher}'

class Schedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=256)
    start_date = models.DateField()

    def __str__(self):
        return f'{self.name} ({self.id})'

class SchedulePause(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    start_date = models.DateField()
    end_date = models.DateField()
    schedule = models.ForeignKey(Schedule, on_delete=models.SET_DEFAULT, default=None)

    def __str__(self):
        return f'{self.schedule.name}: {self.start_date} to {self.end_date}'
