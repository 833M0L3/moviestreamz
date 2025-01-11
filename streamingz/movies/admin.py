from django.contrib import admin
from .models import Video
# Register your models here.

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Video._meta.get_fields()
        if not (field.many_to_many or field.one_to_many)
    ]