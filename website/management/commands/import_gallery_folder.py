import re
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from website.models import GalleryCategory, GalleryImage, GallerySubcategory

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp"}


def slugify_stem(stem: str) -> str:
    value = stem.strip().lower().replace(" ", "-")
    value = re.sub(r"[^a-z0-9-]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "photo"


def pretty_title(stem: str) -> str:
    return re.sub(r"^_+", "", stem).strip()


def source_sort_key(path: Path):
    name = path.stem.upper()
    if re.match(r"^DAN\s*III", name):
        group = 3
    elif re.match(r"^DAN\s*II", name):
        group = 2
    elif re.match(r"^DAN\s*I\b", name):
        group = 1
    elif name.startswith("FMZ"):
        group = 4
    else:
        group = 5
    return (group, name)


def convert_to_webp(src: Path, dest: Path, max_edge: int, quality: int) -> None:
    from PIL import Image, ImageOps

    with Image.open(src) as image:
        image = ImageOps.exif_transpose(image)
        if image.mode != "RGB":
            image = image.convert("RGB")
        width, height = image.size
        longest = max(width, height)
        if longest > max_edge:
            scale = max_edge / longest
            image = image.resize(
                (round(width * scale), round(height * scale)),
                Image.Resampling.LANCZOS,
            )
        dest.parent.mkdir(parents=True, exist_ok=True)
        image.save(dest, "WEBP", quality=quality, method=6)


class Command(BaseCommand):
    help = "Convert a photo folder to WebP and attach it to a gallery subcategory."

    def add_arguments(self, parser):
        parser.add_argument("source", help="Folder with original photos")
        parser.add_argument("--category-slug", default="festival")
        parser.add_argument("--category-name", default="Festival")
        parser.add_argument("--sub-slug", default="festival-1")
        parser.add_argument("--sub-name", default="Festival 1")
        parser.add_argument("--max-edge", type=int, default=1800)
        parser.add_argument("--quality", type=int, default=78)
        parser.add_argument("--order", type=int, default=0, help="Category order")

    def handle(self, *args, **options):
        source = Path(options["source"])
        if not source.is_absolute():
            source = settings.BASE_DIR / source
        if not source.is_dir():
            raise CommandError(f"Folder not found: {source}")

        files = sorted(
            (p for p in source.iterdir() if p.suffix.lower() in IMAGE_EXTS),
            key=source_sort_key,
        )
        if not files:
            raise CommandError(f"No images in {source}")

        dest_dir = (
            settings.BASE_DIR
            / "static"
            / "img"
            / "gallery"
            / options["sub_slug"]
        )
        dest_dir.mkdir(parents=True, exist_ok=True)
        for old in dest_dir.glob("*.webp"):
            old.unlink()

        category, _ = GalleryCategory.objects.get_or_create(
            slug=options["category_slug"],
            defaults={
                "name_sr": options["category_name"],
                "name_en": options["category_name"],
                "name_fr": options["category_name"],
                "order": options["order"],
                "is_active": True,
            },
        )
        subcategory, _ = GallerySubcategory.objects.get_or_create(
            category=category,
            slug=options["sub_slug"],
            defaults={
                "name_sr": options["sub_name"],
                "name_en": options["sub_name"],
                "name_fr": options["sub_name"],
                "order": 1,
                "is_active": True,
            },
        )
        GalleryImage.objects.filter(subcategory=subcategory).delete()

        created = 0
        for index, src in enumerate(files, start=1):
            filename = f"{index:02d}-{slugify_stem(src.stem)}.webp"
            dest = dest_dir / filename
            self.stdout.write(f"  {src.name} -> {filename}")
            convert_to_webp(src, dest, options["max_edge"], options["quality"])
            title = f"{options['sub_name']} — {pretty_title(src.stem)}"
            GalleryImage.objects.create(
                subcategory=subcategory,
                title_sr=title,
                title_en=title,
                title_fr=title,
                image_url=f"/static/img/gallery/{options['sub_slug']}/{filename}",
                order=index,
                is_active=True,
            )
            created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported {created} photos into {category.name_sr} > {subcategory.name_sr}."
            )
        )
