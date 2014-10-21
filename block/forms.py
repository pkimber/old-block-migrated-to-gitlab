# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from block.models import ContentModel


class ContentEmptyForm(forms.ModelForm):

    class Meta:
        model = ContentModel
        fields = ()
