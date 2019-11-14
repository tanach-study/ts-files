from django.contrib import admin

# Register your models here.
from .models import Teacher, Teamim, Classes

class ClassesAdmin(admin.ModelAdmin):
    pass


ClassesAdmin.search_fields=['division', 'segment', 'section', 'unit', 'part']
admin.site.register(Teacher)
admin.site.register(Teamim)
admin.site.register(Classes, ClassesAdmin)
