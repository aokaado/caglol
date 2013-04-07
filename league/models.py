from __future__ import division
from django.db import models
from datetime import datetime
import time
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from smart_selects.db_fields import ChainedForeignKey


class Player(models.Model):
    ROLES = (
        ('t', 'Top'),
        ('j', 'Jungle'),
        ('m', 'Mid'),
        ('a', 'AD-Carry'),
        ('s', 'Support'),
        ('b', 'Sub'),
        ('u', 'Unknown'),
    )
    name = models.CharField(max_length=20, unique=True)
    realname = models.CharField(max_length=60, blank=True)
    role = models.CharField(max_length=1, choices=ROLES, default='u')

    def __unicode__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=30)
    short = models.CharField(max_length=10, unique=True)
    icon = models.FileField(upload_to="team_icons", max_length=50, null=True)
    player = models.ManyToManyField(Player)

    def player_names(self):
        return ', '.join([p.name for p in self.player.all()])

    def is_valid(self):
        return self.player.count() >= 5

    def __unicode__(self):
        return self.name


class Match(models.Model):
    league = models.ForeignKey('League')
    teamone = ChainedForeignKey('league.team', middle='league.standings', related_name="match_team_one", chained_field='league', chained_model_field='league', show_all=False)
    teamtwo = ChainedForeignKey('league.team', middle='league.standings', related_name="match_team_two", chained_field='league', chained_model_field='league', show_all=False)
    teamonescore = models.IntegerField(default=0)
    teamtwoscore = models.IntegerField(default=0)
    date = models.DateField(default=lambda: datetime.now(), blank=True)

    def __unicode__(self):
        status = " #Unplayed#" if not self.has_winner() else ""
        return self.league.short + " " + str(self.date) + " " + self.teamone.short + " vs " + self.teamtwo.short + status

    def has_winner(self):
        if self.teamonescore > self.teamtwoscore:
            self.winner = self.teamone
            self.loser = self.teamtwo
            return True
        elif self.teamtwoscore > self.teamonescore:
            self.winner = self.teamtwo
            self.loser = self.teamone
            return True
        return False

    def apply_update(self):
        winteam = Standings.objects.get(league=self.league, team=self.winner)
        loseteam = Standings.objects.get(league=self.league, team=self.loser)
        #print "Applying standingsupdate to "+str(winteam)+" and "+str(loseteam)
        winteam.wins += 1
        winteam.calc_score()
        loseteam.losses += 1
        loseteam.calc_score()
        winteam.save()
        loseteam.save()

    def revert(self, oldmatch):
        #print "Reverting standingsupdate on"+str(oldmatch.winner)+" and "+str(oldmatch.loser)
        winteam = Standings.objects.get(league=self.league, team=oldmatch.winner)
        loseteam = Standings.objects.get(league=self.league, team=oldmatch.loser)
        winteam.wins -= 1
        winteam.calc_score()
        winteam.save()
        loseteam.losses -= 1
        loseteam.calc_score()
        loseteam.save()

    def update_teams(self):
        oldscore = None
        try:
            oldscore = Match.objects.get(pk=self.id)
        except:
            # This is a new match, just apply results
            if self.has_winner():
                self.apply_update()
            return

        if oldscore.has_winner():
            if self.has_winner() and oldscore.winner == self.winner:
                # Same winner
                None
            else:
                # Revert last then add new if there was a winner
                self.revert(oldscore)
                if self.has_winner():
                    self.apply_update()
        elif not oldscore.has_winner() and self.has_winner():
                self.apply_update()

    def save(self, *args, **kwargs):
        self.update_teams()
        super(Match, self).save(*args, **kwargs)

    @receiver(pre_delete)
    def delete_match(sender, instance, **kwargs):
        if isinstance(instance, Match):
            if instance.has_winner():
                instance.revert(instance)


class League(models.Model):
    name = models.CharField(max_length=30)
    short = models.CharField(max_length=10)
    flavor = models.TextField()
    splash = models.FileField(upload_to="leagues", default="leagues/default.png")

    def __unicode__(self):
        return self.name


class Standings(models.Model):
    league = models.ForeignKey(League)
    team = models.ForeignKey(Team)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    # Should not be neccesary to run this, it's here for initializing the db
    # and as a backup if the scorecount becomes inconsistent
    def update(self):
        start = time.clock()
        matches = Match.objects.filter(league=self.league)
        self.wins = 0
        self.losses = 0

        for match in matches:
            if (match.teamone == self.team and match.teamonescore > match.teamtwoscore) or (match.teamtwo == self.team and match.teamtwoscore > match.teamonescore):
                self.wins += 1
            elif (match.teamone == self.team or match.teamtwo == self.team) and not match.teamonescore == match.teamtwoscore:
                self.losses += 1

        self.calc_score()
        self.save()
        end = time.clock()
        print "updated: "+str(self)+" in "+str(end-start)+" seconds."

    def calc_score(self):
        if self.wins == 0:
            self.score = 0
        else:
            self.score = self.wins/(self.wins + self.losses)*100

    def __unicode__(self):
        return self.league.name+"."+self.team.name

    class Meta:
        unique_together = ('league', 'team')
