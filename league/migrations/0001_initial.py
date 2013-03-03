# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Player'
        db.create_table('league_player', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('league', ['Player'])

        # Adding model 'Team'
        db.create_table('league_team', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('win', self.gf('django.db.models.fields.IntegerField')()),
            ('loss', self.gf('django.db.models.fields.IntegerField')()),
            ('rank', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('league', ['Team'])

        # Adding M2M table for field player on 'Team'
        db.create_table('league_team_player', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('team', models.ForeignKey(orm['league.team'], null=False)),
            ('player', models.ForeignKey(orm['league.player'], null=False))
        ))
        db.create_unique('league_team_player', ['team_id', 'player_id'])

        # Adding model 'Match'
        db.create_table('league_match', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('teamone', self.gf('django.db.models.fields.related.ForeignKey')(related_name='match_team_one', to=orm['league.Team'])),
            ('teamtwo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='match_team_two', to=orm['league.Team'])),
            ('winner', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('league', ['Match'])

        # Adding model 'League'
        db.create_table('league_league', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('league', ['League'])

        # Adding M2M table for field team on 'League'
        db.create_table('league_league_team', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('league', models.ForeignKey(orm['league.league'], null=False)),
            ('team', models.ForeignKey(orm['league.team'], null=False))
        ))
        db.create_unique('league_league_team', ['league_id', 'team_id'])

        # Adding M2M table for field matches on 'League'
        db.create_table('league_league_matches', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('league', models.ForeignKey(orm['league.league'], null=False)),
            ('match', models.ForeignKey(orm['league.match'], null=False))
        ))
        db.create_unique('league_league_matches', ['league_id', 'match_id'])


    def backwards(self, orm):
        
        # Deleting model 'Player'
        db.delete_table('league_player')

        # Deleting model 'Team'
        db.delete_table('league_team')

        # Removing M2M table for field player on 'Team'
        db.delete_table('league_team_player')

        # Deleting model 'Match'
        db.delete_table('league_match')

        # Deleting model 'League'
        db.delete_table('league_league')

        # Removing M2M table for field team on 'League'
        db.delete_table('league_league_team')

        # Removing M2M table for field matches on 'League'
        db.delete_table('league_league_matches')


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
            'teamtwo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'match_team_two'", 'to': "orm['league.Team']"}),
            'winner': ('django.db.models.fields.IntegerField', [], {})
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
