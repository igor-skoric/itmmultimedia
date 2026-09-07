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


def yt_thumb(video_id: str) -> str:
    return f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"


DEFAULT_VIDEO_THUMB = "/static/img/shots/hero-camera.png"

PROJECTS = [
    {
        "title_sr": "Off Road Monster Rožaje",
        "title_en": "Off Road Monster Rožaje",
        "title_fr": "Off Road Monster Rožaje",
        "description_sr": "Off-road trka u Rožajama — teren, tempo i kadar koji prati mašine u pokretu.",
        "description_en": "Off-road race in Rožaje — terrain, pace and a frame that follows the machines in motion.",
        "description_fr": "Course off-road à Rožaje — le terrain, le rythme et un plan qui suit les machines en mouvement.",
        "category": Video.Category.EVENT,
        "year": 2026,
        "source": Video.Source.YOUTUBE,
        "thumb_url": yt_thumb("z2NQZ8h2AV4"),
        "youtube_id": "z2NQZ8h2AV4",
        "order": 1,
    },
    {
        "title_sr": "Džipijada Sjenica 2026",
        "title_en": "Jeep gathering Sjenica 2026",
        "title_fr": "Rassemblement jeep Sjenica 2026",
        "description_sr": "Džipijada Sjenica 2026 u 4K — staza, publika i atmosfera dana.",
        "description_en": "Sjenica 2026 in 4K — the track, the crowd and the feel of the day.",
        "description_fr": "Sjenica 2026 en 4K — la piste, le public et l’atmosphère du jour.",
        "category": Video.Category.EVENT,
        "year": 2026,
        "source": Video.Source.YOUTUBE,
        "thumb_url": yt_thumb("z1g0H6CqqqA"),
        "youtube_id": "z1g0H6CqqqA",
        "order": 2,
    },
    {
        "title_sr": "Hajla nema kočnice",
        "title_en": "Hajla has no brakes",
        "title_fr": "Hajla n’a pas de frein",
        "description_sr": "Džipijada Rožaje 2026 — Hajla bez kočnice, kadar koji prati ritam staze.",
        "description_en": "Rožaje 2026 — Hajla with no brakes, a frame that follows the rhythm of the track.",
        "description_fr": "Rožaje 2026 — Hajla sans frein, un plan qui suit le rythme de la piste.",
        "category": Video.Category.EVENT,
        "year": 2026,
        "source": Video.Source.YOUTUBE,
        "thumb_url": yt_thumb("KOLLFj_9rKw"),
        "youtube_id": "KOLLFj_9rKw",
        "order": 3,
    },
    {
        "title_sr": "Od divljaka do prvaka | Drift | Adrian Adri Petričević",
        "title_en": "From wild one to champion | Drift | Adrian Adri Petričević",
        "title_fr": "Du sauvage au champion | Drift | Adrian Adri Petričević",
        "description_sr": "Podcast sa Adrianom Adri Petričevićem — kralj drifta s Balkana, od garaže do staze.",
        "description_en": "A podcast with Adrian Adri Petričević — the Balkan drift king, from garage to track.",
        "description_fr": "Un podcast avec Adrian Adri Petričević — le roi du drift des Balkans, du garage à la piste.",
        "category": Video.Category.INTERVIEW,
        "year": 2026,
        "source": Video.Source.YOUTUBE,
        "thumb_url": yt_thumb("S7hrOja7GXE"),
        "youtube_id": "S7hrOja7GXE",
        "order": 4,
    },
]


def gallery_still(name: str) -> str:
    return f"/static/img/gallery/beograd-moto-fest/{name}.webp"


NEWS = [
    {
        "slug": "beograd-moto-fest-galerija",
        "kicker": NewsArticle.Kicker.GALLERY,
        "title_sr": "Beograd Moto Fest: kadrovi sa tri dana festivala",
        "title_en": "Belgrade Moto Fest: frames from three festival days",
        "title_fr": "Belgrade Moto Fest : des plans sur trois jours de festival",
        "excerpt_sr": "Galerija je online. Devedeset fotografija sa scene, staze i noći — prvi komplet kadrova sa Beograd Moto Festa.",
        "excerpt_en": "The gallery is live. Ninety photographs from the stage, the track and the night — the first full set of frames from Belgrade Moto Fest.",
        "excerpt_fr": "La galerie est en ligne. Quatre-vingt-dix photographies de la scène, de la piste et de la nuit — le premier ensemble de plans du Belgrade Moto Fest.",
        "body_sr": (
            "Tri dana festivala, jedan ritam: scena, motor, publika. Snimali smo Beograd Moto Fest od prvog kadra do poslednjeg svetla — "
            "koncerte, stazu, detalje na rezervuaru i trenutke kad se noć prelomi u baklju farova.\n\n"
            "Galerija sada nosi 90 fotografija. Nisu svi kadrovi još ušli u selekciju; novi stillovi će se dodavati kako montaža i arhiva napreduju. "
            "Aktuelnosti ostaju mesto gde prvo izlazi šta je spremno za gledanje.\n\n"
            "Ako tražiš atmosferu dana, kreni od galerije. Ako tražiš pokret, projekti nose video sa terena."
        ),
        "body_en": (
            "Three festival days, one rhythm: stage, engine, crowd. We shot Belgrade Moto Fest from the first frame to the last light — "
            "concerts, the track, tank details and the moment night breaks into a flare of headlights.\n\n"
            "The gallery now holds 90 photographs. Not every frame is in the cut yet; new stills will land as the edit and archive move forward. "
            "News stays the place where what is ready to watch appears first.\n\n"
            "If you want the feel of the day, start in the gallery. If you want motion, the projects hold the field video."
        ),
        "body_fr": (
            "Trois jours de festival, un seul rythme : la scène, le moteur, le public. Nous avons filmé le Belgrade Moto Fest du premier plan à la dernière lumière — "
            "concerts, piste, détails de réservoir et l’instant où la nuit se brise en un éclair de phares.\n\n"
            "La galerie compte désormais 90 photographies. Tous les plans ne sont pas encore dans la sélection ; de nouveaux stills arriveront à mesure que le montage avance. "
            "Les actualités restent l’endroit où ce qui est prêt à voir paraît d’abord.\n\n"
            "Pour l’atmosphère du jour, commencez par la galerie. Pour le mouvement, les projets portent la vidéo de terrain."
        ),
        "image_url": gallery_still("65-fmz00845"),
        "published_at": date(2026, 8, 25),
    },
    {
        "slug": "off-road-rozaje-sjenica",
        "kicker": NewsArticle.Kicker.VIDEO,
        "title_sr": "Off-road vikend: Rožaje i Sjenica u kadru",
        "title_en": "Off-road weekend: Rožaje and Sjenica in frame",
        "title_fr": "Week-end off-road : Rožaje et Sjenica au cadre",
        "excerpt_sr": "Tri nova videa sa terena — Off Road Monster, Džipijada Sjenica i Hajla bez kočnice. Pokret, prašina i ritam staze.",
        "excerpt_en": "Three new field videos — Off Road Monster, the Sjenica gathering and Hajla with no brakes. Motion, dust and the rhythm of the track.",
        "excerpt_fr": "Trois nouvelles vidéos de terrain — Off Road Monster, le rassemblement de Sjenica et Hajla sans frein. Mouvement, poussière et rythme de la piste.",
        "body_sr": (
            "Staza ne čeka kadar. Na off-road vikendu radili smo brzo: Rožaje, Sjenica, Hajla — tri priče, isti nagon da se mašina prati u pokretu, "
            "a ne da se samo zabeleži da se događaj desio.\n\n"
            "Off Road Monster nosi teren i tempo. Džipijada Sjenica 2026 ide u 4K, sa publikom i atmosferom dana. Hajla nema kočnice — kadar koji drži ritam staze.\n\n"
            "Videa su na strani projekata. Montaža ostalih klipova je još u toku; kad budu spremni, prvo će se pojaviti ovde."
        ),
        "body_en": (
            "The track does not wait for the frame. On the off-road weekend we worked fast: Rožaje, Sjenica, Hajla — three stories, the same drive to follow the machine in motion "
            "instead of only recording that the event happened.\n\n"
            "Off Road Monster carries the terrain and the pace. The Sjenica 2026 gathering goes out in 4K, with the crowd and the feel of the day. Hajla has no brakes — a frame that holds the rhythm of the track.\n\n"
            "The videos live on the projects page. Other cuts are still in progress; when they are ready, they will appear here first."
        ),
        "body_fr": (
            "La piste n’attend pas le plan. Pendant le week-end off-road, nous avons travaillé vite : Rožaje, Sjenica, Hajla — trois histoires, la même envie de suivre la machine en mouvement "
            "plutôt que de seulement noter que l’événement a eu lieu.\n\n"
            "Off Road Monster porte le terrain et le tempo. Le rassemblement de Sjenica 2026 part en 4K, avec le public et l’atmosphère du jour. Hajla n’a pas de frein — un plan qui tient le rythme de la piste.\n\n"
            "Les vidéos sont sur la page projets. D’autres montages sont encore en cours ; dès qu’ils seront prêts, ils paraîtront ici d’abord."
        ),
        "image_url": yt_thumb("z2NQZ8h2AV4"),
        "published_at": date(2026, 8, 20),
    },
    {
        "slug": "adri-petricevic-intervju",
        "kicker": NewsArticle.Kicker.INTERVIEW,
        "title_sr": "Od divljaka do prvaka: Adri Petričević",
        "title_en": "From wild one to champion: Adri Petričević",
        "title_fr": "Du sauvage au champion : Adri Petričević",
        "excerpt_sr": "Podcast sa kraljem drifta s Balkana — od garaže do staze, bez kočnice. Intervju je sada u projektima.",
        "excerpt_en": "A podcast with the Balkan drift king — from garage to track, with no brakes. The interview is now in projects.",
        "excerpt_fr": "Un podcast avec le roi du drift des Balkans — du garage à la piste, sans frein. L’interview est désormais dans les projets.",
        "body_sr": (
            "Adri Petričević ne priča o kočenju. U ovoj epizodi ide se od garaže do staze: počeci, novac i trud iza jednog drift auta, "
            "anekdote sa trka i ono što ga drži da ide bočno napred.\n\n"
            "Intervju je format u kojem kadar mora da drži lice, tišinu i tempo priče. Zato je ovo u projektima kao intervju, a ne kao highlight trke.\n\n"
            "Pusti epizodu na strani projekata — i vrati se ovde kad izađe sledeći razgovor."
        ),
        "body_en": (
            "Adri Petričević does not talk about braking. This episode runs from garage to track: beginnings, the money and work behind a drift car, "
            "race anecdotes and what keeps him going sideways.\n\n"
            "An interview is a format where the frame has to hold a face, a silence and the pace of the story. That is why this sits in projects as an interview, not as a race highlight.\n\n"
            "Play the episode on the projects page — and come back here when the next conversation lands."
        ),
        "body_fr": (
            "Adri Petričević ne parle pas de freiner. Cet épisode va du garage à la piste : les débuts, l’argent et le travail derrière une voiture de drift, "
            "les anecdotes de course et ce qui le pousse à avancer en glisse.\n\n"
            "L’interview est un format où le plan doit tenir un visage, un silence et le tempo du récit. C’est pourquoi elle est classée comme interview, pas comme highlight de course.\n\n"
            "Lancez l’épisode sur la page projets — et revenez ici dès que la prochaine conversation paraîtra."
        ),
        "image_url": yt_thumb("S7hrOja7GXE"),
        "published_at": date(2026, 8, 18),
    },
    {
        "slug": "u-radu-sledeci-kadar",
        "kicker": NewsArticle.Kicker.IN_PROGRESS,
        "title_sr": "U radu: sledeći kadar još nije gotov",
        "title_en": "In progress: the next frame is not done yet",
        "title_fr": "En cours : le prochain plan n’est pas encore fini",
        "excerpt_sr": "Montaža traje. Novi stillovi i klipovi ulaze čim budu spremni — aktuelnosti su dnevnik terena, ne arhiva na čekanju.",
        "excerpt_en": "The cut is still moving. New stills and clips land as soon as they are ready — news is the field journal, not an archive on hold.",
        "excerpt_fr": "Le montage avance encore. Nouveaux stills et clips dès qu’ils sont prêts — les actualités sont le journal de terrain, pas une archive en attente.",
        "body_sr": (
            "Ne čekamo da sve bude savršeno pa da onda objavimo. Aktuelnosti su stranica na kojoj se vidi rad dok još traje: šta je ušlo u galeriju, "
            "šta je montirano, šta tek dolazi.\n\n"
            "Ako danas nema nove vesti, to ne znači da nema terena. Znači da je kadar još u timeline-u. Vrati se ovde — sledeći unos izlazi čim priča dobije oblik."
        ),
        "body_en": (
            "We do not wait for everything to be perfect before we publish. News is the page where the work is visible while it is still happening: what entered the gallery, "
            "what has been cut, what is still coming.\n\n"
            "If there is no new post today, that does not mean there is no field. It means the frame is still on the timeline. Come back — the next entry lands as soon as the story takes shape."
        ),
        "body_fr": (
            "Nous n’attendons pas que tout soit parfait pour publier. Les actualités sont la page où le travail se voit pendant qu’il se fait : ce qui est entré dans la galerie, "
            "ce qui a été monté, ce qui arrive encore.\n\n"
            "S’il n’y a pas de nouveau texte aujourd’hui, cela ne veut pas dire qu’il n’y a pas de terrain. Cela veut dire que le plan est encore sur la timeline. Revenez — la prochaine note paraît dès que l’histoire prend forme."
        ),
        "image_url": gallery_still("81-slo2168"),
        "published_at": date(2026, 8, 12),
    },
]


class Command(BaseCommand):
    help = "Seed demo content for ITM Multimedia"

    def add_arguments(self, parser):
        parser.add_argument(
            "--only",
            choices=["videos", "news"],
            help="Reseed only one content type (does not wipe the rest).",
        )

    def handle(self, *args, **options):
        if options.get("only") == "videos":
            self.seed_videos()
            self.stdout.write(self.style.SUCCESS("Projects seeded successfully."))
            return
        if options.get("only") == "news":
            self.seed_news()
            self.stdout.write(self.style.SUCCESS("News seeded successfully."))
            return

        self.stdout.write("Seeding demo data...")

        GalleryImage.objects.all().delete()
        GallerySubcategory.objects.all().delete()
        GalleryCategory.objects.all().delete()
        Partner.objects.all().delete()

        self.seed_gallery_album(
            slug="beograd-moto-fest",
            name_sr="Beograd Moto Fest",
            name_en="Belgrade Moto Fest",
            name_fr="Belgrade Moto Fest",
            order=0,
        )
        self.seed_gallery_album(
            slug="ostalo",
            name_sr="Ostalo",
            name_en="Other",
            name_fr="Autre",
            order=1,
        )

        self.seed_news()
        self.seed_videos()

        partners = [
            {
                "name": "IT Branch",
                "url": "https://itbranch.rs/",
                "logo_url": "/static/img/partners/it-branch-logo.png",
                "image_url": "/static/img/partners/it-branch.jpg",
                "description_sr": "Web aplikacije, sajtovi i digitalna rešenja. Partner sa kojim povezujemo kadar, identitet i digitalno iskustvo — od sajta do alata koji prate produkciju.",
                "description_en": "Web apps, websites and digital solutions. A partner we connect frame, identity and digital experience with — from the site to the tools around production.",
                "description_fr": "Applications web, sites et solutions digitales. Un partenaire avec qui nous relions le plan, l’identité et l’expérience digitale — du site aux outils de production.",
                "order": 1,
            },
            {
                "name": "Arena Live",
                "url": "https://example.com",
                "image_url": shot("concert"),
                "description_sr": "Live produkcija koncerata i specijalnih večeri. Zajedno beležimo scenu, publiku i trenutak kad svetlo, zvuk i kadar postanu jedna priča.",
                "description_en": "Live production for concerts and special nights. Together we capture the stage, the crowd and the moment when light, sound and frame become one story.",
                "description_fr": "Production live pour concerts et soirées spéciales. Ensemble, nous saisissons la scène, le public et l’instant où lumière, son et plan ne font plus qu’une histoire.",
                "order": 2,
            },
            {
                "name": "Pulse Audio",
                "url": "https://example.org",
                "image_url": shot("audio"),
                "description_sr": "Tonska produkcija za emisije, intervjue i live formate. Čist ton, pravi ritam i atmosfera koja nosi kadar — od seta do finalnog mixa.",
                "description_en": "Sound production for shows, interviews and live formats. Clean tone, the right rhythm and an atmosphere that carries the frame — from set to final mix.",
                "description_fr": "Production son pour émissions, interviews et formats live. Un son net, le bon rythme et une atmosphère qui porte le plan — du plateau au mix final.",
                "order": 3,
            },
            {
                "name": "Lumen Lights",
                "url": "https://example.net",
                "image_url": shot("lights"),
                "description_sr": "Osvetljenje koje gradi atmosferu kadra. Od scene i studija do detalja u kadru — svetlo koje vodi pogled i emociju.",
                "description_en": "Lighting that shapes the atmosphere of the frame. From stage and studio to the detail in shot — light that guides the eye and the feeling.",
                "description_fr": "Une lumière qui construit l’atmosphère du plan. De la scène et du studio au détail dans le cadre — une lumière qui guide le regard et l’émotion.",
                "order": 4,
            },
        ]
        for data in partners:
            Partner.objects.create(**data)

        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully."))

    def seed_videos(self):
        Video.objects.all().delete()
        for data in PROJECTS:
            Video.objects.create(
                **{**data, "thumb_url": data.get("thumb_url") or DEFAULT_VIDEO_THUMB}
            )
        self.stdout.write(f"Seeded {len(PROJECTS)} projects.")

    def seed_news(self):
        NewsArticle.objects.all().delete()
        for data in NEWS:
            NewsArticle.objects.create(**data)
        self.stdout.write(f"Seeded {len(NEWS)} news articles.")

    def seed_gallery_album(self, slug, name_sr, name_en, name_fr, order):
        category = GalleryCategory.objects.create(
            slug=slug,
            name_sr=name_sr,
            name_en=name_en,
            name_fr=name_fr,
            order=order,
        )
        album = GallerySubcategory.objects.create(
            category=category,
            slug=slug,
            name_sr=name_sr,
            name_en=name_en,
            name_fr=name_fr,
            order=1,
        )
        gallery_dir = settings.BASE_DIR / "static" / "img" / "gallery" / slug
        if not gallery_dir.is_dir():
            return
        count = 0
        for i, path in enumerate(sorted(gallery_dir.glob("*.webp")), start=1):
            title = f"{name_sr} — {path.stem.split('-', 1)[-1]}"
            GalleryImage.objects.create(
                subcategory=album,
                title_sr=title,
                title_en=title,
                title_fr=title,
                image_url=f"/static/img/gallery/{slug}/{path.name}",
                order=i,
            )
            count += 1
        self.stdout.write(f"Seeded {count} photos into {name_sr}.")
