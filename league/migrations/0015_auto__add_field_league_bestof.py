# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'League.bestof'
        db.add_column('league_league', 'bestof',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'League.bestof'
        db.delete_column('league_league', 'bestof')


    models = {
        'league.league': {
            'Meta': {'object_name': 'League'},
            'bestof': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'flavor': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'short': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'splash': ('django.db.models.fields.files.FileField', [], {'default': "'leagues/default.png'", 'max_length': '100'})
        },
        'league.match': {
            'Meta': {'object_name': 'Match'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 5, 1, 0, 0)', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['league.League']"}),
            'teamone': ('smart_selects.db_fields.ChainedForeignKey', [], {'related_name': "'match_team_one'", 'to': "orm['league.Team']"}),
            'teamonescore': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'teamtwo': ('smart_selects.db_fields.ChainedForeignKey', [], {'related_name': "'match_team_two'", 'to': "orm['league.Team']"}),
            'teamtwoscore': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'league.player': {
            'Meta': {'object_name': 'Player'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'realname': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'u'", 'max_length': '1'})
        },
        'league.standings': {
            'Meta': {'unique_together': "(('league', 'team'),)", 'object_name': 'Standings'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['league.League']"}),
            'losses': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['league.Team']"}),
            'wins': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'league.team': {
            'Meta': {'object_name': 'Team'},
            'icon': ('django.db.models.fields.files.FileField', [], {'max_length': '50', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'player': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['league.Player']", 'symmetrical': 'False'}),
            'short': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'})
        }
    }

    complete_apps = ['league']