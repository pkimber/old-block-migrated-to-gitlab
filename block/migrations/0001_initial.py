# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EditState'
        db.create_table('block_editstate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
        ))
        db.send_create_signal('block', ['EditState'])

        # Adding model 'ModerateState'
        db.create_table('block_moderatestate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
        ))
        db.send_create_signal('block', ['ModerateState'])

        # Adding model 'Page'
        db.create_table('block_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('slug_menu', self.gf('django.db.models.fields.SlugField')(blank=True, max_length=100)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_home', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('template_name', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal('block', ['Page'])

        # Adding unique constraint on 'Page', fields ['slug', 'slug_menu']
        db.create_unique('block_page', ['slug', 'slug_menu'])

        # Adding model 'Section'
        db.create_table('block_section', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
            ('block_app', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('block_model', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('create_url_name', self.gf('django.db.models.fields.CharField')(blank=True, max_length=100)),
        ))
        db.send_create_signal('block', ['Section'])

        # Adding model 'PageSection'
        db.create_table('block_pagesection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['block.Page'])),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['block.Section'])),
        ))
        db.send_create_signal('block', ['PageSection'])

        # Adding unique constraint on 'PageSection', fields ['page', 'section']
        db.create_unique('block_pagesection', ['page_id', 'section_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'PageSection', fields ['page', 'section']
        db.delete_unique('block_pagesection', ['page_id', 'section_id'])

        # Removing unique constraint on 'Page', fields ['slug', 'slug_menu']
        db.delete_unique('block_page', ['slug', 'slug_menu'])

        # Deleting model 'EditState'
        db.delete_table('block_editstate')

        # Deleting model 'ModerateState'
        db.delete_table('block_moderatestate')

        # Deleting model 'Page'
        db.delete_table('block_page')

        # Deleting model 'Section'
        db.delete_table('block_section')

        # Deleting model 'PageSection'
        db.delete_table('block_pagesection')


    models = {
        'block.editstate': {
            'Meta': {'object_name': 'EditState', 'ordering': "['name']"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
        },
        'block.moderatestate': {
            'Meta': {'object_name': 'ModerateState', 'ordering': "['name']"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
        },
        'block.page': {
            'Meta': {'object_name': 'Page', 'unique_together': "(('slug', 'slug_menu'),)", 'ordering': "['order', 'slug', 'slug_menu']"},
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_home': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'slug_menu': ('django.db.models.fields.SlugField', [], {'blank': 'True', 'max_length': '100'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'block.pagesection': {
            'Meta': {'object_name': 'PageSection', 'unique_together': "(('page', 'section'),)", 'ordering': "('page__slug', 'section__slug')"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['block.Page']"}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['block.Section']"})
        },
        'block.section': {
            'Meta': {'object_name': 'Section', 'ordering': "('name',)"},
            'block_app': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'block_model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'create_url_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['block']