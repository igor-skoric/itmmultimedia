from django.contrib import admin

from .models import (
    ContactMessage,
    GalleryCategory,
    GalleryImage,
    GallerySubcategory,
    NewsArticle,
    Partner,
    Video,
)


class GallerySubcategoryInline(admin.TabularInline):
    model = GallerySubcategory
    extra = 0


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ("name_sr", "slug", "order", "is_active")
    list_editable = ("order", "is_active")
    prepopulated_fields = {"slug": ("name_sr",)}
    inlines = [GallerySubcategoryInline]


@admin.register(GallerySubcategory)
class GallerySubcategoryAdmin(admin.ModelAdmin):
    list_display = ("name_sr", "category", "slug", "order", "is_active")
    list_filter = ("category", "is_active")
    list_editable = ("order", "is_active")
    prepopulated_fields = {"slug": ("name_sr",)}


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title_sr", "subcategory", "order", "is_active", "created_at")
    list_filter = ("subcategory__category", "subcategory", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title_sr", "title_en", "title_fr")


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ("title_sr", "kicker", "published_at", "is_published")
    list_filter = ("kicker", "is_published")
    list_editable = ("kicker", "is_published")
    prepopulated_fields = {"slug": ("title_sr",)}
    search_fields = ("title_sr", "title_en", "title_fr")


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title_sr", "category", "year", "source", "order", "is_active")
    list_filter = ("category", "year", "source", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title_sr", "title_en", "title_fr")


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name", "description_sr")
    fields = (
        "name",
        "url",
        "logo_url",
        "image_url",
        "description_sr",
        "description_en",
        "description_fr",
        "order",
        "is_active",
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "is_read", "created_at")
    list_filter = ("is_read",)
    list_editable = ("is_read",)
    search_fields = ("name", "email", "phone", "message")
    readonly_fields = ("name", "email", "phone", "message", "created_at")
