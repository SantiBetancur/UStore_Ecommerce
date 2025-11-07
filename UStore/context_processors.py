from django.utils import translation


def i18n_debug(request):
    """Context processor that exposes i18n debug info to templates.

    Provides:
      - I18N_DEBUG_LANGUAGE_CODE: current active language according to django.translation
      - I18N_DEBUG_REQUEST_LANGUAGE: request.LANGUAGE_CODE if set on the request
      - I18N_DEBUG_COOKIE: value of the 'django_language' cookie
    """
    return {
        "I18N_DEBUG_LANGUAGE_CODE": translation.get_language(),
        "I18N_DEBUG_REQUEST_LANGUAGE": getattr(request, "LANGUAGE_CODE", None),
        "I18N_DEBUG_COOKIE": request.COOKIES.get("django_language"),
    }
