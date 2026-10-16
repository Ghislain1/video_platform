from django.contrib import admin

from videos.models import Category, Video

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "access_type", "price", "is_published", "created_at")
    list_filter = ("category", "access_type", "is_published")
    search_fields = ("title", "description")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Video Information", { "fields": ("title", "description", "category", "video_file", "thumbnail")}),
        ("Access and pricing", { "fields": ("access_type", "price")}),
        ("Publication", { "fields": ("is_published", "created_at", "updated_at")}),
    )