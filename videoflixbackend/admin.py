from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Video, VideoQuality

# Register your models here.



class VideoQualityInline(admin.TabularInline):
    model = VideoQuality
    extra = 1  # Wie viele leere Felder standardmäßig angezeigt werden sollen

class VideoAdmin(admin.ModelAdmin):
    inlines = [
        VideoQualityInline,
    ]

admin.site.register(Video, VideoAdmin)
