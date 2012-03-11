from django.contrib import admin

from orderable.admin import OrderableTabularInline

from models import Gallery, Image

class ImageInline(OrderableTabularInline):
    model = Image
    extra = 0

class GalleryAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline
    ]

admin.site.register(Gallery, GalleryAdmin)