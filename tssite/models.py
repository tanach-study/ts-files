from django.db import models
from .validators import validate_file_extension
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from tssite import client


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
        instance.division == 'tere_asar'
    ):
        base = ''
        if instance.division == 'neviim_rishonim':
            base = 'archives/Neviim%20Rishonim'
        elif instance.division == 'neviim_aharonim':
            base = 'archives/Neviim%20Aharonim'
        elif instance.division == 'tere_asar':
            base = 'archives/Tere%20Asar'

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
        path = f"{base}/{instance.section_title.replace(' ', '%20')}/{file}.mp3"

    elif instance.division == 'parasha':
        base = 'archives/parasha'
        path = f'{base}/{instance.segment}/{instance.segment}-{instance.section}-{instance.unit}-{instance.teacher.teacher_string}.mp3'

    elif instance.division == 'mishna':
        base = 'archives/mishna'
        file = f'{instance.segment}-{instance.section}-{instance.unit}-{instance.part}-{instance.teacher.teacher_string}'
        path = f'{base}/{instance.segment}/{instance.section}/{file}.mp3'

    else:
        raise Exception('invalid division')

    return path

def create_transcoder_job(audio_field):
    if client is None:
        raise Exception("client not initialized")

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
    print("created encoder job")

class Class(models.Model):
    division = models.CharField(max_length=256)
    division_name = models.CharField(max_length=256, null=True, blank=True)
    division_title = models.CharField(max_length=256, null=True, blank=True)
    division_sponsor = models.CharField(max_length=256, null=True, blank=True)
    division_sequence = models.CharField(max_length=256, null=True, blank=True)
    segment = models.CharField(max_length=256)
    segment_name = models.CharField(max_length=256, null=True, blank=True)
    segment_title = models.CharField(max_length=256, null=True, blank=True)
    segment_sponsor = models.CharField(max_length=256, null=True, blank=True)
    segment_sequence = models.CharField(max_length=256, null=True, blank=True)
    section = models.CharField(max_length=256)
    section_name = models.CharField(max_length=256, null=True, blank=True)
    section_title = models.CharField(max_length=256, null=True, blank=True)
    section_sponsor = models.CharField(max_length=256, null=True, blank=True)
    section_sequence = models.CharField(max_length=256, null=True, blank=True)
    unit = models.CharField(max_length=256)
    unit_name = models.CharField(max_length=256, null=True, blank=True)
    unit_title = models.CharField(max_length=256, null=True, blank=True)
    unit_sponsor = models.CharField(max_length=256, null=True, blank=True)
    unit_sequence = models.CharField(max_length=256, null=True, blank=True)
    part = models.CharField(max_length=256, null=True, blank=True)
    part_name = models.CharField(max_length=256, null=True, blank=True)
    part_title = models.CharField(max_length=256, null=True, blank=True)
    part_sponsor = models.CharField(max_length=256, null=True, blank=True)
    part_sequence = models.CharField(max_length=256, null=True, blank=True)
    series = models.CharField(max_length=256, null=True, blank=True)
    series_name = models.CharField(max_length=256, null=True, blank=True)
    series_title = models.CharField(max_length=256, null=True, blank=True)
    series_sponsor = models.CharField(max_length=256, null=True, blank=True)
    series_sequence = models.CharField(max_length=256, null=True, blank=True)
    start_chapter = models.CharField(max_length=256, null=True, blank=True)
    start_verse = models.CharField(max_length=256, null=True, blank=True)
    end_chapter = models.CharField(max_length=256, null=True, blank=True)
    end_verse = models.CharField(max_length=256, null=True, blank=True)
    audio_url = models.CharField(max_length=1024, null=True, blank=True)
    audio = models.FileField(upload_to=get_class_audio_location, validators=[validate_file_extension], default=None, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_DEFAULT, default=None, null=True)
    date = models.DateTimeField(null=True, blank=True)
    video_url = models.CharField(max_length=1024, null=True, blank=True)

    class Meta:
        ordering = ['series_sequence', 'division_sequence', 'segment_sequence', 'section_sequence', 'unit_sequence', 'part_sequence']

    def __str__(self):
        audio = get_class_audio_location(self, '')
        toreturn = ''

        if self.division == 'torah':
            toreturn = f'Torah - Sefer {self.section_title} Parashat {self.unit_title}: Part {self.part}'
        elif (
            self.division == 'neviim_rishonim' or
            self.division == 'neviim_aharonim' or
            self.division == 'tere_asar' or
            self.division == 'ketuvim'
        ):
            if self.part:
                toreturn = f'{self.division_title} - Sefer {self.section_title}: Perek {self.unit.title()} Part {self.part}'
            else:
                toreturn = f'{self.division_title} - Sefer {self.section_title}: Perek {self.unit.title()}'

        elif self.division == 'parasha':
            if self.part:
                toreturn = f'{self.division.title()} - {self.segment_title}: {self.section_title} {self.unit.title()} {self.part}'
            else:
                toreturn = f'{self.division.title()} - {self.segment_title}: {self.section_title} {self.unit.title()}'

        elif self.division == 'mishna':
            toreturn = f'{self.division_title} - {self.segment_title}: {self.section_title} Perek {self.unit.title()} Mishna {self.part}'
        return toreturn


@receiver(post_save, sender=Class, dispatch_uid="update_class")
def update_class(sender, instance, created, raw, using, update_fields, **kwargs):
    if created or (update_fields and 'audio' in update_fields):
        create_transcoder_job(instance.audio)



class Teamim(models.Model):
    reader = models.ForeignKey(Teacher, on_delete=models.SET_DEFAULT, default=None, null=True)
    audio = models.FileField(upload_to='uploads/', null=True, blank=True)
    post = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)

