from django.contrib import admin

# Register your models here.
from .models import Teacher, Teamim, Class

class ClassAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        update_fields = []
        if change:
            if form.initial['audio'] != form.cleaned_data['audio']:
                update_fields.append('audio')

        obj.save(update_fields=update_fields)


ClassAdmin.search_fields=['division', 'segment', 'section', 'unit', 'part']
admin.site.register(Teacher)
admin.site.register(Teamim)
admin.site.register(Class, ClassAdmin)
