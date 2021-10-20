from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Project)

admin.site.register(models.Review)

admin.site.register(models.Tag)
admin.site.register(models.Profile)
admin.site.register(models.Skill)
admin.site.register(models.Message)
