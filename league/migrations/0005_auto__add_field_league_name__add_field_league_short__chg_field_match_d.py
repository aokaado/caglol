# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'League.name'
        db.add_column('league_league', 'name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30),
                      keep_default=False)

        # Adding field 'League.short'
        db.add_column('league_league', 'short',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=10),
                      keep_default=False)


        # Changing field 'Match.date'
        db.alter_column('league_match', 'date', self.gf('django.db.models.fields.DateField')(auto_now_add=True))
        # Deleting field 'Team.loss'
        db.delete_column('league_team', 'loss')

        # Deleting field 'Team.win'
        db.delete_column('league_team', 'win')

        # Deleting field 'Team.rank'
        db.delete_column('league_team', 'rank')


    def backwards(self, orm):
        # Deleting field 'League.name'
        db.delete_column('league_league', 'name')

        # Deleting field 'League.short'
        db.delete_column('league_league', 'short')


        # Changing field 'Match.date'
        db.alter_column('league_match', 'date', self.gf('django.db.models.fields.DateField')())
        # Adding field 'Team.loss'
        db.add_column('league_team', 'loss',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Team.win'
        db.add_column('league_team', 'win',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Team.rank'
        db.add_column('league_team', 'rank',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    models = {
        'league.league': {
            'Meta': {'object_name': 'League'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matches': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['league.Match']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'short': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'team': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['league.Team']", 'symmetrical': 'False'})
        },
        'league.match': {
            'Meta': {'object_name': 'Match'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'teamone': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'match_team_one'", 'to': "orm['league.Team']"}),
            'teamonescore': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'teamtwo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'match_team_two'", 'to': "orm['league.Team']"}),
            'teamtwoscore': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'player': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['league.Player']", 'symmetrical': 'False'}),
            'short': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['league']