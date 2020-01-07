from django.contrib import admin

# Register your models here.
from .models import Project, Library, ItemRecord, Instruction, Feature, Exclusion, BddAdmin, ReplyMail

admin.site.register(Project)
admin.site.register(Library)
admin.site.register(ItemRecord)
admin.site.register(Instruction)
admin.site.register(Feature)
admin.site.register(Exclusion)
admin.site.register(BddAdmin)
admin.site.register(ReplyMail)
