from django.core.cache import cache
from django.db import models
from .helpers import import_item
from django.utils.html import strip_tags
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from .options_settings import OPTION_CLASS, TEXT_CLASS, LABEL_CLASS


class OptionCache(object):
    langs_cache_key = 'qoptlangs'

    @staticmethod
    def _getkey(key, lang=None):
        if lang is None:
            lang = get_language()
        return "qopt_%s_%s" % (key, lang)

    @staticmethod
    def get(key):
        return cache.get(OptionCache._getkey(key), None)

    @staticmethod
    def set(key, value):
        lang = get_language()
        langs = cache.get(OptionCache.langs_cache_key, set()) or set()
        langs.add(lang)
        cache.set(OptionCache.langs_cache_key, langs)

        cache.set(OptionCache._getkey(key), value)

    @staticmethod
    def delete(key):
        cache.delete(OptionCache._getkey(key))

    @staticmethod
    def delete_all_langs(key):
        for lang in cache.get(OptionCache.langs_cache_key, set()):
            cache.delete(OptionCache._getkey(key, lang))


class OptionAbstract(models.Model):
    """
    Options model
    """
    key = models.CharField(_('Key'), max_length=50, unique=True)
    value = models.CharField(_('Value'), max_length=256, blank=True)

    cache_mask = 'qo_o_{0}'

    class Meta:
        verbose_name = _('option')
        verbose_name_plural = _('options')
        ordering = ['key']
        abstract = True

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            OptionCache.delete_all_langs(OptionAbstract.cache_mask.format(self.key))
        except KeyError:
            pass


class LabelAbstract(models.Model):
    key = models.CharField(_('Key'), max_length=50, unique=True)
    value = models.CharField(_('Value'), max_length=256, blank=True)

    cache_mask = 'qo_l_{0}'

    class Meta:
        verbose_name = _('label')
        verbose_name_plural = _('labels')
        ordering = ['key']
        abstract = True

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            OptionCache.delete_all_langs(LabelAbstract.cache_mask.format(self.key))
        except KeyError:
            pass


class TextAbstract(models.Model):
    key = models.CharField(_('Key'), max_length=50, unique=True)
    notes = models.TextField(_('Notes'), default='', blank=True)
    title = models.CharField(_('Title'), max_length=256, blank=True)
    text = models.TextField(_('Text'))

    cache_mask = 'qo_t_{0}'

    class Meta:
        verbose_name = _('text')
        verbose_name_plural = _('texts')
        ordering = ['key']
        abstract = True

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            OptionCache.delete_all_langs(TextAbstract.cache_mask.format(self.key))
        except KeyError:
            pass

    def get_notes_without_tags(self):
        return strip_tags(self.notes)
    get_notes_without_tags.short_description = 'Notes'


class Option(import_item(OPTION_CLASS) if OPTION_CLASS else OptionAbstract):
    pass


class Label(import_item(LABEL_CLASS) if LABEL_CLASS else LabelAbstract):
    pass


class Text(import_item(TEXT_CLASS) if TEXT_CLASS else TextAbstract):
    pass
