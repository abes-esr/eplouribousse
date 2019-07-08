from django.contrib import admin

# Register your models here.
from .models import Project, Library, ItemRecord, Instruction, Feature, Exclusion

admin.site.register(Project)
admin.site.register(Library)
admin.site.register(ItemRecord)
admin.site.register(Instruction)
admin.site.register(Feature)
admin.site.register(Exclusion)
