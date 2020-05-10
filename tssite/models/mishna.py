from django.db import models
from tssite.validators import validate_file_extension
from django.conf import settings
from tssite import client
from .common import Teacher, Sponsor

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

def get_mishna_audio_location(instance, filename):
    base = 'archives/mishna'
    file = f'{instance.segment}-{instance.section}-{instance.unit}-{instance.part}-{instance.teacher.teacher_string}'
    path = f'{base}/{instance.segment}/{instance.section}/{file}.mp3'
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

class MishnaSeder(models.Model):
    name = models.CharField(max_length=256)
    sequence = models.SmallIntegerField()
    sponsor = models.ForeignKey(Sponsor, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True)

    def __str__(self):
        return f'Seder {self.name.title()}'

class MishnaMasechet(models.Model):
    name = models.CharField(max_length=256)
    sequence = models.SmallIntegerField()
    sponsor = models.ForeignKey(Sponsor, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True)

    def __str__(self):
        return f'Masechet {self.name.title()}'

class MishnaStudy(models.Model):
    seder = models.ForeignKey(MishnaSeder, on_delete=models.CASCADE)
    masechet = models.ForeignKey(MishnaMasechet, on_delete=models.CASCADE)
    perek = models.IntegerField()
    mishna = models.IntegerField()
    title = models.CharField(max_length=256)
    audio = models.FileField(upload_to=get_mishna_audio_location, validators=[validate_file_extension], default=None, null=True, max_length=500)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_DEFAULT, default=None, null=True)
    date = models.DateTimeField(null=True, blank=True)

    def get_location(self):
        return f'/mishna-study/perek/{self.seder.name}/{self.massechet.name}/{self.perek}?part={self.mishna}'

    def __str__(self):
        return f'Masechet {self.masechet.title()}: Perek {self.perek} Mishna {self.mishna}'
