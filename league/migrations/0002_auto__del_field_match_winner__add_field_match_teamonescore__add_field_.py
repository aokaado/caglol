# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Match.winner'
        db.delete_column('league_match', 'winner')

        # Adding field 'Match.teamonescore'
        db.add_column('league_match', 'teamonescore',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Match.teamtwoscore'
        db.add_column('league_match', 'teamtwoscore',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Match.winner'
        db.add_column('league_match', 'winner',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'Match.teamonescore'
        db.delete_column('league_match', 'teamonescore')

        # Deleting field 'Match.teamtwoscore'
        db.delete_column('league_match', 'teamtwoscore')


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'league.team': {
            'Meta': {'object_name': 'Team'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loss': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'player': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['league.Player']", 'symmetrical': 'False'}),
            'rank': ('django.db.models.fields.IntegerField', [], {}),
            'win': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['league']