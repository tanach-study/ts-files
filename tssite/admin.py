from django.contrib import admin

# Register your models here.
from .models import Teacher, Teamim, Class, TalmudSponsor, TalmudStudy

class ClassAdmin(admin.ModelAdmin):
    search_fields=['division', 'segment', 'section', 'unit', 'part']


admin.site.register(Teacher)
admin.site.register(Teamim)
admin.site.register(Class, ClassAdmin)
admin.site.register(TalmudSponsor)
admin.site.register(TalmudStudy)
