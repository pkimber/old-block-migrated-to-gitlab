# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PaginatedSection'
        db.create_table('block_paginatedsection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('items_per_page', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('order_by_field', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('block', ['PaginatedSection'])

        # Adding field 'Section.paginated'
        db.add_column('block_section', 'paginated',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['block.PaginatedSection']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'PaginatedSection'
        db.delete_table('block_paginatedsection')

        # Deleting field 'Section.paginated'
        db.delete_column('block_section', 'paginated_id')


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
        'block.paginatedsection': {
            'Meta': {'object_name': 'PaginatedSection'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items_per_page': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'order_by_field': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'paginated': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['block.PaginatedSection']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True'})
        }
    }

    complete_apps = ['block']