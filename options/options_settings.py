from django.conf import settings

CREATE_ITEMS = getattr(settings, 'OPTIONS_CREATE_ITEMS', False)
OPTION_CLASS = getattr(settings, 'OPTIONS_OPTION_CLASS', None)
TEXT_CLASS = getattr(settings, 'OPTIONS_TEXT_CLASS', None)
LABEL_CLASS = getattr(settings, 'OPTIONS_LABEL_CLASS', None)
