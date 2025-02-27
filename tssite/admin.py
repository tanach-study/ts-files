from django.contrib import admin

# Register your models here.
from .models import Teacher, Teamim, Class, TalmudSponsor, TalmudStudy, Schedule, SchedulePause
from .models import create_transcoder_job

class ClassAdmin(admin.ModelAdmin):
    search_fields = ['division', 'segment', 'section', 'unit', 'part', 'series']
    list_display = ['__str__', 'division', 'segment', 'section', 'unit', 'part', 'series', 'date']

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


class TeamimAdmin(admin.ModelAdmin):
    search_fields = ['post', 'reader']
    raw_id_fields = ('post', 'reader',)
    list_display = ('post', 'reader',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if 'audio' in form.changed_data and obj.audio:
            if change:
                print('creating encoder job for existing object', str(obj))
            else:
                print('creating encoder job for new object', str(obj))
            create_transcoder_job(obj.audio)

class SchedulePauseInline(admin.TabularInline):
    model = SchedulePause

class ScheduleAdmin(admin.ModelAdmin):
    inlines = [
        SchedulePauseInline,
    ]


admin.site.register(Teacher)
admin.site.register(Teamim, TeamimAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(TalmudSponsor)
admin.site.register(TalmudStudy, TalmudStudyAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(SchedulePause)
