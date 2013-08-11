# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Lesson'
        db.create_table(u'main_lesson', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('description', self.gf('tinymce.models.HTMLField')()),
            ('expect', self.gf('django.db.models.fields.TextField')()),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('max_score', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'main', ['Lesson'])

        # Adding model 'Answer'
        db.create_table(u'main_answer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Lesson'])),
            ('result', self.gf('django.db.models.fields.TextField')()),
            ('score', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('advice', self.gf('tinymce.models.HTMLField')()),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'main', ['Answer'])

        # Adding model 'Hint'
        db.create_table(u'main_hint', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Lesson'])),
            ('description', self.gf('tinymce.models.HTMLField')()),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
            ('level', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'main', ['Hint'])

        # Adding model 'HintUsage'
        db.create_table(u'main_hintusage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hint', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Hint'])),
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Answer'])),
        ))
        db.send_create_signal(u'main', ['HintUsage'])

        # Adding unique constraint on 'HintUsage', fields ['hint', 'answer']
        db.create_unique(u'main_hintusage', ['hint_id', 'answer_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'HintUsage', fields ['hint', 'answer']
        db.delete_unique(u'main_hintusage', ['hint_id', 'answer_id'])

        # Deleting model 'Lesson'
        db.delete_table(u'main_lesson')

        # Deleting model 'Answer'
        db.delete_table(u'main_answer')

        # Deleting model 'Hint'
        db.delete_table(u'main_hint')

        # Deleting model 'HintUsage'
        db.delete_table(u'main_hintusage')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'main.answer': {
            'Meta': {'object_name': 'Answer'},
            'advice': ('tinymce.models.HTMLField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Lesson']"}),
            'result': ('django.db.models.fields.TextField', [], {}),
            'score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'main.hint': {
            'Meta': {'object_name': 'Hint'},
            'description': ('tinymce.models.HTMLField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Lesson']"}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        u'main.hintusage': {
            'Meta': {'unique_together': "(('hint', 'answer'),)", 'object_name': 'HintUsage'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Answer']"}),
            'hint': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Hint']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'main.lesson': {
            'Meta': {'object_name': 'Lesson'},
            'description': ('tinymce.models.HTMLField', [], {}),
            'expect': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_score': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['main']