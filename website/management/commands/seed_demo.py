from datetime import date

from django.conf import settings
from django.core.management.base import BaseCommand

from website.models import (
    GalleryCategory,
    GalleryImage,
    GallerySubcategory,
    NewsArticle,
    Partner,
    Video,
)


def shot(name: str) -> str:
    return f"/static/img/shots/{name}.jpg"


PROJECTS = [
    {
        "title_sr": "Noć pod reflektorima",
        "title_en": "Night under the lights",
        "title_fr": "Nuit sous les projecteurs",
        "description_sr": "Aftermovie sa glavne scene — publika, svetlo i ritam koncerta u jednom kadru.",
        "description_en": "Main-stage aftermovie — crowd, light and the rhythm of the night in one cut.",
        "description_fr": "Aftermovie de la scène principale — public, lumière et rythme du concert.",
        "category": Video.Category.EVENT,
        "year": 2025,
        "source": Video.Source.YOUTUBE,
        "thumb_url": shot("concert"),
        "youtube_id": "ScMzIvxBSi4",
        "order": 1,
    },
    {
        "title_sr": "Derbi. 90 minuta.",
        "title_en": "Derby. 90 minutes.",
        "title_fr": "Derby. 90 minutes.",
        "description_sr": "Sport u pokretu: tribine, tempo utakmice i trenutak koji ostaje.",
        "description_en": "Sport in motion: the stands, the pace of the match, the frame that stays.",
        "description_fr": "Le sport en mouvement : tribunes, rythme du match, l’image qui reste.",
        "category": Video.Category.EVENT,
        "year": 2025,
        "source": Video.Source.YOUTUBE,
        "thumb_url": shot("football"),
        "youtube_id": "tgbNymZ7vqY",
        "order": 2,
    },
    {
        "title_sr": "Studio razgovor",
        "title_en": "Studio conversation",
        "title_fr": "Conversation en studio",
        "description_sr": "Intervju vođen atmosferom seta i pričom sagovornika.",
        "description_en": "An interview shaped by the set and the guest’s story.",
        "description_fr": "Un entretien porté par l’atmosphère du plateau et le récit de l’invité.",
        "category": Video.Category.INTERVIEW,
        "year": 2026,
        "source": Video.Source.YOUTUBE,
        "thumb_url": shot("conference-talk"),
        "youtube_id": "jNQXAC9IVRw",
        "order": 3,
    },
    {
        "title_sr": "Emisija u kadru",
        "title_en": "Show in frame",
        "title_fr": "Émission en cadre",
        "description_sr": "TV i online format — od ideje i seta do montaže i odjavne špice.",
        "description_en": "A TV and online format — from idea and set to the final edit.",
        "description_fr": "Un format TV et online — de l’idée et du plateau au montage final.",
        "category": Video.Category.SHOW,
        "year": 2026,
        "source": Video.Source.YOUTUBE,
        "thumb_url": shot("conference"),
        "youtube_id": "M7lc1UVf-VE",
        "order": 4,
    },
    {
        "title_sr": "Brand u pokretu",
        "title_en": "Brand in motion",
        "title_fr": "Marque en mouvement",
        "description_sr": "Kratki promotivni film: identitet, emocija i kadar koji nosi poruku.",
        "description_en": "A short promo film: identity, emotion and a frame that carries the message.",
        "description_fr": "Un court film promo : identité, émotion et un plan qui porte le message.",
        "category": Video.Category.PROMO,
        "year": 2025,
        "source": Video.Source.LOCAL,
        "thumb_url": shot("event"),
        "local_src": "https://videos.pexels.com/video-files/3195394/3195394-hd_1280_720_25fps.mp4",
        "order": 5,
    },
    {
        "title_sr": "Stories sa terena",
        "title_en": "Stories from the field",
        "title_fr": "Stories du terrain",
        "description_sr": "Kratki kadrovi za društvene mreže, u ritmu samog događaja.",
        "description_en": "Short cuts for social — in the rhythm of the event itself.",
        "description_fr": "Plans courts pour les réseaux, au rythme de l’événement.",
        "category": Video.Category.SOCIAL,
        "year": 2026,
        "source": Video.Source.INSTAGRAM,
        "thumb_url": shot("promo"),
        "instagram_url": "https://www.instagram.com/",
        "order": 6,
    },
    {
        "title_sr": "Aftermovie: jesenja scena",
        "title_en": "Aftermovie: autumn stage",
        "title_fr": "Aftermovie : scène d’automne",
        "description_sr": "Kompletna priča događaja — od prvog kadra do poslednjeg tona.",
        "description_en": "The full story of the night — from the first frame to the last note.",
        "description_fr": "L’histoire complète de la soirée — du premier plan à la dernière note.",
        "category": Video.Category.EVENT,
        "year": 2024,
        "source": Video.Source.LOCAL,
        "thumb_url": shot("festival-night"),
        "local_src": "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4",
        "order": 7,
    },
    {
        "title_sr": "Novi format",
        "title_en": "New format",
        "title_fr": "Nouveau format",
        "description_sr": "Specijalni kreativni projekat — ideja koja tek pronalazi svoj kadar.",
        "description_en": "A special creative project — an idea still finding its frame.",
        "description_fr": "Un projet créatif spécial — une idée qui trouve encore son cadre.",
        "category": Video.Category.SPECIAL,
        "year": 2026,
        "source": Video.Source.INSTAGRAM,
        "thumb_url": shot("theatre"),
        "instagram_url": "https://www.instagram.com/",
        "order": 8,
    },
]


class Command(BaseCommand):
    help = "Seed demo content for ITM Multimedia"

    def add_arguments(self, parser):
        parser.add_argument(
            "--only",
            choices=["videos"],
            help="Reseed only one content type (does not wipe the rest).",
        )

    def handle(self, *args, **options):
        if options.get("only") == "videos":
            self.seed_videos()
            self.stdout.write(self.style.SUCCESS("Projects seeded successfully."))
            return

        self.stdout.write("Seeding demo data...")

        GalleryImage.objects.all().delete()
        GallerySubcategory.objects.all().delete()
        GalleryCategory.objects.all().delete()
        NewsArticle.objects.all().delete()
        Partner.objects.all().delete()

        festival = GalleryCategory.objects.create(
            slug="festival",
            name_sr="Festival",
            name_en="Festival",
            name_fr="Festival",
            order=0,
        )
        festival_1 = GallerySubcategory.objects.create(
            category=festival,
            slug="festival-1",
            name_sr="Festival 1",
            name_en="Festival 1",
            name_fr="Festival 1",
            order=1,
        )
        festival_dir = settings.BASE_DIR / "static" / "img" / "gallery" / "festival-1"
        if festival_dir.is_dir():
            for i, path in enumerate(sorted(festival_dir.glob("*.webp")), start=1):
                title = f"Festival 1 — {path.stem.split('-', 1)[-1]}"
                GalleryImage.objects.create(
                    subcategory=festival_1,
                    title_sr=title,
                    title_en=title,
                    title_fr=title,
                    image_url=f"/static/img/gallery/festival-1/{path.name}",
                    order=i,
                )

        NewsArticle.objects.create(
            slug="nova-sezona-koncerata",
            title_sr="Nova sezona koncerata: otvaramo veliku jesenju scenu",
            title_en="New concert season: opening the autumn stage",
            title_fr="Nouvelle saison de concerts : ouverture de la scène d’automne",
            excerpt_sr="Najavljujemo seriju događaja koje ćemo organizovati i dokumentovati kroz galeriju i video arhivu.",
            excerpt_en="Announcing a series of events we will organize and document through gallery and video archives.",
            excerpt_fr="Annonce d’une série d’événements que nous organiserons et documenterons via galerie et archives vidéo.",
            body_sr=(
                "Jesenja sezona donosi kombinaciju open-air i dvoranskih produkcija. ITM Multimedia preuzima kompletnu organizaciju — od produkcije do promocije i medijske arhive.\n\n"
                "Publika će kroz galeriju moći da prati svaki događaj po kategorijama, a kroz aktuelnosti dobija najave, reportaže i behind-the-scenes materijale.\n\n"
                "Sadržaj se sada uređuje kroz Django admin panel."
            ),
            body_en=(
                "The autumn season mixes open-air and venue productions. ITM Multimedia handles full organization — from production to promotion and media archive.\n\n"
                "Audiences will follow every event by category in the gallery, while news brings announcements, reports and behind-the-scenes stories.\n\n"
                "Content is now managed through the Django admin panel."
            ),
            body_fr=(
                "La saison d’automne mélange productions en plein air et en salle. ITM Multimedia assure l’organisation complète — de la production à la promotion et aux archives média.\n\n"
                "Le public suivra chaque événement par catégorie dans la galerie, tandis que les actualités apportent annonces, reportages et coulisses.\n\n"
                "Le contenu se gère désormais via le panneau d’administration Django."
            ),
            image_url=shot("crowd"),
            published_at=date(2026, 8, 2),
        )
        NewsArticle.objects.create(
            slug="sportski-vikend-u-fokusu",
            title_sr="Sportski vikend u fokusu kamere",
            title_en="A sports weekend in camera focus",
            title_fr="Un week-end sportif sous l’objectif",
            excerpt_sr="Dva dana, više arena — foto i video ekipa na terenu za kompletnu pokrivenost.",
            excerpt_en="Two days, multiple arenas — photo and video teams covering every angle.",
            excerpt_fr="Deux jours, plusieurs arènes — équipes photo et vidéo sur tous les angles.",
            body_sr=(
                "Sportski događaji zahtevaju brzinu i preciznost. Naš tim radi paralelno: galerija se puni po podkategorijama, dok video ide na YouTube i lokalni server.\n\n"
                "Cilj je da publika i partneri istog dana imaju pristup najboljim kadrovima i highlight snimcima."
            ),
            body_en=(
                "Sports events demand speed and precision. Our team works in parallel: the gallery fills by subcategory while video goes to YouTube and the local server.\n\n"
                "The goal is same-day access to the best frames and highlight reels for audiences and partners."
            ),
            body_fr=(
                "Les événements sportifs exigent vitesse et précision. Notre équipe travaille en parallèle : la galerie se remplit par sous-catégorie, la vidéo part sur YouTube et le serveur local.\n\n"
                "L’objectif : un accès le jour même aux meilleures images et aux highlights."
            ),
            image_url=shot("sport"),
            published_at=date(2026, 7, 18),
        )
        NewsArticle.objects.create(
            slug="korporativni-launch-beograd",
            title_sr="Korporativni launch u Beogradu",
            title_en="Corporate launch in Belgrade",
            title_fr="Lancement corporate à Belgrade",
            excerpt_sr="Kompletan brand doživljaj: scena, sadržaj, galerija i kratki film sa događaja.",
            excerpt_en="A full brand experience: stage, content, gallery and a short event film.",
            excerpt_fr="Une expérience de marque complète : scène, contenu, galerie et court film.",
            body_sr=(
                "Za korporativne partnere radimo end-to-end: koncepcija, produkcija događaja i sadržaj za kanale komunikacije.\n\n"
                "Na sajtu, launch eventi imaju posebnu podkategoriju u galeriji i poseban video izvor kada materijal ostaje lokalno na serveru."
            ),
            body_en=(
                "For corporate partners we deliver end-to-end: concept, event production and content for communication channels.\n\n"
                "On the site, launch events get a dedicated gallery subcategory and a local video source when media stays on the server."
            ),
            body_fr=(
                "Pour les partenaires corporate, nous livrons de bout en bout : concept, production et contenus pour les canaux de communication.\n\n"
                "Sur le site, les lancements ont une sous-catégorie dédiée et une source vidéo locale lorsque les médias restent sur le serveur."
            ),
            image_url=shot("promo"),
            published_at=date(2026, 6, 30),
        )

        self.seed_videos()

        partners = [
            {
                "name": "IT Branch",
                "url": "https://itbranch.rs/",
                "logo_url": "/static/img/partners/it-branch-logo.png",
                "image_url": "/static/img/partners/it-branch.jpg",
                "description_sr": (
                    "IT Branch projektuje, razvija i održava web aplikacije, sajtove i digitalna rešenja "
                    "fokusirana na prodaju, automatizaciju i merljive rezultate — od prve ideje do produkcije."
                ),
                "description_en": (
                    "IT Branch designs, builds and maintains web apps, websites and digital solutions "
                    "focused on sales, automation and measurable results — from the first idea to production."
                ),
                "description_fr": (
                    "IT Branch conçoit, développe et maintient des applications web, des sites et des solutions digitales "
                    "orientés vente, automatisation et résultats mesurables — de la première idée à la mise en production."
                ),
                "order": 1,
            },
            {
                "name": "Arena Live",
                "url": "https://example.com",
                "image_url": shot("concert"),
                "description_sr": (
                    "Produkcija uživo: scene, ritam događaja i kadrovi koji prenose energiju publike. "
                    "Zajedno pokrivamo koncerte i specijalne večeri od pripreme do aftermovie-a."
                ),
                "description_en": (
                    "Live production: stages, the rhythm of the event and frames that carry the crowd. "
                    "Together we cover concerts and special nights from prep to the aftermovie."
                ),
                "description_fr": (
                    "Production live : scènes, rythme de l’événement et plans qui portent l’énergie du public. "
                    "Ensemble, nous couvrons concerts et soirées spéciales, de la préparation à l’aftermovie."
                ),
                "order": 2,
            },
            {
                "name": "Pulse Audio",
                "url": "https://example.org",
                "image_url": shot("audio"),
                "description_sr": (
                    "Tonska produkcija za emisije, intervjue i live formate. Čist zvuk na setu, "
                    "da slika i priča ostanu u istom ritmu."
                ),
                "description_en": (
                    "Sound production for shows, interviews and live formats. Clean audio on set, "
                    "so picture and story stay in the same rhythm."
                ),
                "description_fr": (
                    "Production son pour émissions, interviews et formats live. Un son propre sur le plateau, "
                    "pour que l’image et l’histoire restent dans le même rythme."
                ),
                "order": 3,
            },
            {
                "name": "Lumen Lights",
                "url": "https://example.net",
                "image_url": shot("lights"),
                "description_sr": (
                    "Osvetljenje koje gradi atmosferu kadra — od studija do otvorene scene. "
                    "Svetlo kao deo priče, ne kao dekoracija."
                ),
                "description_en": (
                    "Lighting that shapes the frame — from studio to open stage. "
                    "Light as part of the story, not decoration."
                ),
                "description_fr": (
                    "Une lumière qui construit l’atmosphère du plan — du studio à la scène ouverte. "
                    "La lumière comme partie de l’histoire, pas comme décor."
                ),
                "order": 4,
            },
        ]
        for data in partners:
            Partner.objects.create(**data)

        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully."))

    def seed_videos(self):
        Video.objects.all().delete()
        for data in PROJECTS:
            Video.objects.create(**data)
        self.stdout.write(f"Seeded {len(PROJECTS)} projects.")
