from django.contrib import admin

from videos.models import Category, Video
from .models import Purchase, VideoAccessGrant
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

@admin.register(VideoAccessGrant)
class VideoAccessGrantAdmin(admin.ModelAdmin):
    list_display = ("user", "video", "source", "granted_at")
    list_filter = ("source", "granted_at")
    search_fields = ("user__username", "video__title")
    autocomplete_fields = ("user", "video")

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "video",
        "amount",
        "currency",
        "status",
        "created_at",
        "paid_at",
    )

    list_filter = (
        "status",
        "currency",
        "created_at",
    )

    search_fields = (
        "user__username",
        "video__title",
        "stripe_checkout_session_id",
    )

    readonly_fields = (
        "amount",
        "currency",
        "stripe_checkout_session_id",
        "stripe_payment_intent_id",
        "created_at",
        "paid_at",
    )