from django.contrib import admin

# Register your models here.
from .models.common import Teacher, Sponsor, Teamim, Class, TalmudSponsor, TalmudStudy
from .models.common import create_transcoder_job
from .models.mishna import MishnaSeder, MishnaMasechet, MishnaStudy

class ClassAdmin(admin.ModelAdmin):
    search_fields=['division', 'segment', 'section', 'unit', 'part']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        update_fields = []
        if change:
            for key in form.initial:
                if form.initial[key] != form.cleaned_data[key]:
                    update_fields.append(key)
            if 'audio' in update_fields:
                print('creating encoder job for', str(obj))
                create_transcoder_job(obj.audio)


class TalmudStudyAdmin(admin.ModelAdmin):
    search_fields=['seder', 'masechet']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        update_fields = []
        if change:
            for key in form.initial:
                if form.initial[key] != form.cleaned_data[key]:
                    update_fields.append(key)
            if 'audio' in update_fields:
                print('creating encoder job for', str(obj))
                create_transcoder_job(obj.audio)


class MishnaStudyAdmin(admin.ModelAdmin):
    search_fields=['seder', 'masechet']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        update_fields = []
        if change:
            for key in form.initial:
                if form.initial[key] != form.cleaned_data[key]:
                    update_fields.append(key)
            if 'audio' in update_fields:
                print('creating encoder job for', str(obj))
                create_transcoder_job(obj.audio)


admin.site.register(Teacher)
admin.site.register(Teamim)
admin.site.register(Class, ClassAdmin)
admin.site.register(TalmudSponsor)
admin.site.register(TalmudStudy, TalmudStudyAdmin)
admin.site.register(MishnaSeder)
admin.site.register(MishnaMasechet)
admin.site.register(MishnaStudy, MishnaStudyAdmin)
