from django import template

from website.i18n_strings import translate

register = template.Library()


@register.simple_tag(takes_context=True)
def ui(context, key, **kwargs):
    lang = context.get("lang", "sr")
    return translate(key, lang, **kwargs)


@register.simple_tag
def loc(obj, field, lang):
    return obj.localized(field, lang)


@register.simple_tag(takes_context=True)
def qs(context, **kwargs):
    request = context.get("request")
    params = request.GET.copy() if request else {}
    for key, value in kwargs.items():
        if value in (None, "") or (key == "page" and str(value) == "1"):
            params.pop(key, None)
        else:
            params[key] = value
    encoded = params.urlencode()
    return f"?{encoded}" if encoded else "?"
