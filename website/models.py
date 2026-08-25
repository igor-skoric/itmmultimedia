from django.db import models


class LocalizedModel(models.Model):
    class Meta:
        abstract = True

    def localized(self, field: str, lang: str) -> str:
        value = getattr(self, f"{field}_{lang}", "") or ""
        if value:
            return value
        return getattr(self, f"{field}_sr", "") or ""


class GalleryCategory(LocalizedModel):
    slug = models.SlugField(unique=True)
    name_sr = models.CharField(max_length=120)
    name_en = models.CharField(max_length=120, blank=True)
    name_fr = models.CharField(max_length=120, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name_plural = "gallery categories"

    def __str__(self):
        return self.name_sr


class GallerySubcategory(LocalizedModel):
    category = models.ForeignKey(
        GalleryCategory, on_delete=models.CASCADE, related_name="subcategories"
    )
    slug = models.SlugField()
    name_sr = models.CharField(max_length=120)
    name_en = models.CharField(max_length=120, blank=True)
    name_fr = models.CharField(max_length=120, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        unique_together = ("category", "slug")
        verbose_name_plural = "gallery subcategories"

    def __str__(self):
        return f"{self.category.name_sr} / {self.name_sr}"


class GalleryImage(LocalizedModel):
    subcategory = models.ForeignKey(
        GallerySubcategory, on_delete=models.CASCADE, related_name="images"
    )
    title_sr = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True)
    title_fr = models.CharField(max_length=200, blank=True)
    image_url = models.URLField(max_length=500)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title_sr


class NewsArticle(LocalizedModel):
    class Kicker(models.TextChoices):
        GALLERY = "gallery", "Galerija"
        VIDEO = "video", "Video"
        INTERVIEW = "interview", "Intervju"
        FIELD = "field", "Teren"
        IN_PROGRESS = "in_progress", "U radu"

    slug = models.SlugField(unique=True)
    title_sr = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255, blank=True)
    title_fr = models.CharField(max_length=255, blank=True)
    excerpt_sr = models.TextField()
    excerpt_en = models.TextField(blank=True)
    excerpt_fr = models.TextField(blank=True)
    body_sr = models.TextField(help_text="Paragrafi odvojeni praznim redom.")
    body_en = models.TextField(blank=True)
    body_fr = models.TextField(blank=True)
    kicker = models.CharField(max_length=20, choices=Kicker.choices, blank=True)
    image_url = models.URLField(max_length=500)
    published_at = models.DateField()
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-published_at", "-id"]
        verbose_name = "aktuelnost"
        verbose_name_plural = "aktuelnosti"

    def __str__(self):
        return self.title_sr

    def body_paragraphs(self, lang: str):
        text = self.localized("body", lang)
        return [p.strip() for p in text.split("\n\n") if p.strip()]

    @property
    def kicker_i18n_key(self):
        return f"news_kicker_{self.kicker}" if self.kicker else ""


class Video(LocalizedModel):
    class Source(models.TextChoices):
        YOUTUBE = "youtube", "YouTube"
        INSTAGRAM = "instagram", "Instagram"
        LOCAL = "local", "Lokalno"

    class Category(models.TextChoices):
        EVENT = "event", "Događaj"
        SHOW = "show", "Emisija"
        INTERVIEW = "interview", "Intervju"
        PROMO = "promo", "Promo"
        SOCIAL = "social", "Društvene mreže"
        SPECIAL = "special", "Specijalni projekat"

    title_sr = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True)
    title_fr = models.CharField(max_length=200, blank=True)
    description_sr = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    description_fr = models.TextField(blank=True)
    category = models.CharField(
        max_length=20, choices=Category.choices, default=Category.EVENT
    )
    year = models.PositiveIntegerField(default=2026)
    source = models.CharField(max_length=20, choices=Source.choices)
    thumb_url = models.URLField(max_length=500)
    youtube_id = models.CharField(max_length=32, blank=True)
    instagram_url = models.URLField(max_length=500, blank=True)
    local_src = models.URLField(max_length=500, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "-id"]
        verbose_name = "projekat"
        verbose_name_plural = "projekti"

    def __str__(self):
        return self.title_sr

    @property
    def category_i18n_key(self):
        return f"project_cat_{self.category}"


class Partner(LocalizedModel):
    name = models.CharField(max_length=120)
    url = models.URLField(max_length=500)
    logo_url = models.URLField(max_length=500, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    description_sr = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    description_fr = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.email}"
