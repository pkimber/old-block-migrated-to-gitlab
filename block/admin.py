# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import (
    Page,
    Section,
)


class PageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Page, PageAdmin)


class SectionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Section, SectionAdmin)
