from django.conf import settings

from .i18n_strings import translate


def get_language(request) -> str:
    lang = request.COOKIES.get(settings.SITE_LANGUAGE_COOKIE) or settings.DEFAULT_SITE_LANGUAGE
    if lang not in settings.SITE_LANGUAGES:
        return settings.DEFAULT_SITE_LANGUAGE
    return lang


def site_i18n(request):
    lang = get_language(request)

    def t(key, **kwargs):
        return translate(key, lang, **kwargs)

    return {
        "lang": lang,
        "languages": settings.SITE_LANGUAGES,
        "t": t,
    }
