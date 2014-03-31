# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Page', fields ['slug']
        db.delete_unique('block_page', ['slug'])

        # Adding field 'Page.slug_menu'
        db.add_column('block_page', 'slug_menu',
                      self.gf('django.db.models.fields.SlugField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding unique constraint on 'Page', fields ['slug', 'slug_menu']
        db.create_unique('block_page', ['slug', 'slug_menu'])


    def backwards(self, orm):
        # Removing unique constraint on 'Page', fields ['slug', 'slug_menu']
        db.delete_unique('block_page', ['slug', 'slug_menu'])

        # Deleting field 'Page.slug_menu'
        db.delete_column('block_page', 'slug_menu')

        # Adding unique constraint on 'Page', fields ['slug']
        db.create_unique('block_page', ['slug'])


    models = {
        'block.editstate': {
            'Meta': {'ordering': "['name']", 'object_name': 'EditState'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
        },
        'block.moderatestate': {
            'Meta': {'ordering': "['name']", 'object_name': 'ModerateState'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
        },
        'block.page': {
            'Meta': {'unique_together': "(('slug', 'slug_menu'),)", 'ordering': "['order', 'slug', 'slug_menu']", 'object_name': 'Page'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_home': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'slug_menu': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'blank': 'True'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'block.section': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Section'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['block']