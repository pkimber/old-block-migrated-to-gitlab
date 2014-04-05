# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PageSection'
        db.create_table('block_pagesection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['block.Page'])),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['block.Section'])),
            ('block_app', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('block_model', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url_name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('block', ['PageSection'])

        # Adding unique constraint on 'PageSection', fields ['page', 'section']
        db.create_unique('block_pagesection', ['page_id', 'section_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'PageSection', fields ['page', 'section']
        db.delete_unique('block_pagesection', ['page_id', 'section_id'])

        # Deleting model 'PageSection'
        db.delete_table('block_pagesection')


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
            'Meta': {'ordering': "['order', 'slug', 'slug_menu']", 'unique_together': "(('slug', 'slug_menu'),)", 'object_name': 'Page'},
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
        'block.pagesection': {
            'Meta': {'ordering': "('page__slug', 'section__slug')", 'unique_together': "(('page', 'section'),)", 'object_name': 'PageSection'},
            'block_app': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'block_model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['block.Page']"}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['block.Section']"}),
            'url_name': ('django.db.models.fields.TextField', [], {})
        },
        'block.section': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Section'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True'})
        }
    }

    complete_apps = ['block']