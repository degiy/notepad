from django.contrib import admin

# Register your models here.

from .models import NDir, NEntry

admin.site.register(NDir)
admin.site.register(NEntry)
