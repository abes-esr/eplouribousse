from django.contrib import admin

# Register your models here.
from .models import Library, ItemRecord, Instruction, Feature

admin.site.register(Library)
admin.site.register(ItemRecord)
admin.site.register(Instruction)
admin.site.register(Feature)
