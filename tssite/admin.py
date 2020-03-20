from django.contrib import admin

# Register your models here.
from .models import Teacher, Teamim, Class, TalmudSponsor, TalmudStudy

class ClassAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        update_fields = []
        if change:
            for key in form.initial:
                if form.initial[key] != form.cleaned_data[key]:
                    update_fields.append(key)

        obj.save(update_fields=update_fields)


ClassAdmin.search_fields=['division', 'segment', 'section', 'unit', 'part']
admin.site.register(Teacher)
admin.site.register(Teamim)
admin.site.register(Class, ClassAdmin)
admin.site.register(TalmudSponsor)
admin.site.register(TalmudStudy)
