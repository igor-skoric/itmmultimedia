from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.db.models import Prefetch, Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_GET, require_http_methods

from .context_processors import get_language
from .i18n_strings import translate
from .models import (
    ContactMessage,
    GalleryCategory,
    GalleryImage,
    GallerySubcategory,
    NewsArticle,
    Partner,
    Video,
)

PAGE_SIZE_GALLERY = 24
PAGE_SIZE_VIDEOS = 6
PAGE_SIZE_NEWS = 2
PAGE_SIZE_PARTNERS = 3


def listing_query(request):
    return (request.GET.get("q") or "").strip()[:80]


def paginate(request, queryset, per_page):
    return Paginator(queryset, per_page).get_page(request.GET.get("page"))


def text_search(queryset, query, *fields, year_field=None):
    if not query:
        return queryset
    combined = Q()
    for field in fields:
        combined |= Q(**{f"{field}__icontains": query})
    if year_field and query.isdigit():
        combined |= Q(**{year_field: int(query)})
    return queryset.filter(combined)


def home(request):
    lang = get_language(request)
    partners = Partner.objects.filter(is_active=True)
    featured_videos = list(Video.objects.filter(is_active=True)[:6])
    return render(
        request,
        "home.html",
        {
            "partners": partners,
            "featured_videos": featured_videos,
            "lang": lang,
        },
    )


def gallery(request):
    lang = get_language(request)
    categories = GalleryCategory.objects.filter(is_active=True).prefetch_related(
        Prefetch(
            "subcategories",
            queryset=GallerySubcategory.objects.filter(is_active=True),
        )
    )
    active_category = request.GET.get("category", "all")
    active_sub = request.GET.get("sub", "all")

    images = GalleryImage.objects.filter(
        is_active=True,
        subcategory__is_active=True,
        subcategory__category__is_active=True,
    ).select_related("subcategory", "subcategory__category")
    if active_category != "all":
        images = images.filter(subcategory__category__slug=active_category)
    if active_sub != "all":
        images = images.filter(subcategory__slug=active_sub)

    current_category = None
    if active_category != "all":
        current_category = next((c for c in categories if c.slug == active_category), None)

    page_obj = paginate(request, images, PAGE_SIZE_GALLERY)

    return render(
        request,
        "gallery.html",
        {
            "categories": categories,
            "images": page_obj,
            "page_obj": page_obj,
            "active_category": active_category,
            "active_sub": active_sub,
            "current_category": current_category,
            "lang": lang,
        },
    )


def news_list(request):
    lang = get_language(request)
    query = listing_query(request)
    articles = NewsArticle.objects.filter(is_published=True)
    articles = text_search(
        articles,
        query,
        "title_sr",
        "title_en",
        "title_fr",
        "excerpt_sr",
        "excerpt_en",
        "excerpt_fr",
        "body_sr",
        "body_en",
        "body_fr",
    )
    page_obj = paginate(request, articles, PAGE_SIZE_NEWS)
    items = list(page_obj.object_list)
    featured = None
    rest = items
    if not query and page_obj.number == 1 and items:
        featured = items[0]
        rest = items[1:]
    return render(
        request,
        "news_list.html",
        {
            "featured": featured,
            "articles": rest,
            "page_obj": page_obj,
            "query": query,
            "lang": lang,
        },
    )


def news_detail(request, slug):
    lang = get_language(request)
    article = get_object_or_404(NewsArticle, slug=slug, is_published=True)
    return render(
        request,
        "news_detail.html",
        {
            "article": article,
            "paragraphs": article.body_paragraphs(lang),
            "lang": lang,
        },
    )


def videos(request):
    lang = get_language(request)
    query = listing_query(request)
    active_category = request.GET.get("category", "all")
    qs = Video.objects.filter(is_active=True)
    if active_category != "all":
        qs = qs.filter(category=active_category)
    qs = text_search(
        qs,
        query,
        "title_sr",
        "title_en",
        "title_fr",
        "description_sr",
        "description_en",
        "description_fr",
        year_field="year",
    )
    page_obj = paginate(request, qs, PAGE_SIZE_VIDEOS)
    return render(
        request,
        "videos.html",
        {
            "videos": page_obj,
            "page_obj": page_obj,
            "categories": Video.Category.choices,
            "active_category": active_category,
            "query": query,
            "lang": lang,
        },
    )


def partners(request):
    lang = get_language(request)
    query = listing_query(request)
    qs = Partner.objects.filter(is_active=True)
    qs = text_search(
        qs,
        query,
        "name",
        "description_sr",
        "description_en",
        "description_fr",
    )
    page_obj = paginate(request, qs, PAGE_SIZE_PARTNERS)
    return render(
        request,
        "partners.html",
        {
            "partners": page_obj,
            "page_obj": page_obj,
            "query": query,
            "lang": lang,
        },
    )


@require_http_methods(["GET", "POST"])
def contact(request):
    lang = get_language(request)
    values = {
        "name": "",
        "email": "",
        "phone": "",
        "message": "",
    }
    errors = {}

    if request.method == "POST":
        for key in values:
            values[key] = (request.POST.get(key) or "").strip()

        if (request.POST.get("company") or "").strip():
            return HttpResponseRedirect(reverse("contact") + "?sent=1")

        if not values["name"]:
            errors["name"] = translate("contact_err_name", lang)
        if not values["email"]:
            errors["email"] = translate("contact_err_email", lang)
        else:
            try:
                validate_email(values["email"])
            except ValidationError:
                errors["email"] = translate("contact_err_email", lang)
        if len(values["message"]) < 8:
            errors["message"] = translate("contact_err_message", lang)

        if not errors:
            ContactMessage.objects.create(
                name=values["name"][:120],
                email=values["email"],
                phone=values["phone"][:40],
                message=values["message"],
            )
            try:
                send_mail(
                    subject=f"ITM kontakt: {values['name']}",
                    message=(
                        f"Ime: {values['name']}\n"
                        f"Email: {values['email']}\n"
                        f"Telefon: {values['phone'] or '-'}\n\n"
                        f"{values['message']}"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[getattr(settings, "CONTACT_EMAIL", "office@itmmultimedia.rs")],
                    fail_silently=False,
                )
            except Exception:
                pass
            return HttpResponseRedirect(reverse("contact") + "?sent=1")

    return render(
        request,
        "contact.html",
        {
            "lang": lang,
            "values": values,
            "errors": errors,
            "sent": request.GET.get("sent") == "1",
        },
    )


@require_GET
def set_language(request):
    lang = request.GET.get("lang", settings.DEFAULT_SITE_LANGUAGE)
    if lang not in settings.SITE_LANGUAGES:
        lang = settings.DEFAULT_SITE_LANGUAGE

    next_url = request.GET.get("next") or request.META.get("HTTP_REFERER") or reverse("home")
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = reverse("home")

    response = HttpResponseRedirect(next_url)
    response.set_cookie(
        settings.SITE_LANGUAGE_COOKIE,
        lang,
        max_age=60 * 60 * 24 * 365,
        samesite="Lax",
    )
    return response
