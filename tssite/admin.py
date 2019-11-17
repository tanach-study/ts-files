from django.contrib import admin

# Register your models here.
from .models import Teacher, Teamim, Class

class ClassAdmin(admin.ModelAdmin):
    pass


ClassAdmin.search_fields=['division', 'segment', 'section', 'unit', 'part']
admin.site.register(Teacher)
admin.site.register(Teamim)
admin.site.register(Class, ClassAdmin)
