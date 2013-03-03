# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Team.short'
        db.add_column('league_team', 'short',
                      self.gf('django.db.models.fields.CharField')(default=' ', max_length=10),
                      keep_default=False)


        # Changing field 'Team.name'
        db.alter_column('league_team', 'name', self.gf('django.db.models.fields.CharField')(max_length=30))

    def backwards(self, orm):
        # Deleting field 'Team.short'
        db.delete_column('league_team', 'short')


        # Changing field 'Team.name'
        db.alter_column('league_team', 'name', self.gf('django.db.models.fields.CharField')(max_length=20))

    models = {
        'league.league': {
            'Meta': {'object_name': 'League'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matches': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['league.Match']", 'symmetrical': 'False'}),
            'team': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['league.Team']", 'symmetrical': 'False'})
        },
        'league.match': {
            'Meta': {'object_name': 'Match'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'teamone': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'match_team_one'", 'to': "orm['league.Team']"}),
            'teamonescore': ('django.db.models.fields.IntegerField', [], {}),
            'teamtwo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'match_team_two'", 'to': "orm['league.Team']"}),
            'teamtwoscore': ('django.db.models.fields.IntegerField', [], {})
        },
        'league.player': {
            'Meta': {'object_name': 'Player'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'u'", 'max_length': '1'})
        },
        'league.team': {
            'Meta': {'object_name': 'Team'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loss': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'player': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['league.Player']", 'symmetrical': 'False'}),
            'rank': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'short': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'win': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['league']