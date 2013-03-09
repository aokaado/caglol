from __future__ import division
from django.db import models
from math import ceil
from league.models import Team
from datetime import datetime
from smart_selects.db_fields import ChainedForeignKey
from tournament.utils import pow2roundup


# TODO perhaps make a "match" superclass
class Matchup(models.Model):
    LEVEL = (
        ('w', 'Winner'),
        ('l', 'Loser'),
    )

    tournament = models.ForeignKey('Tournament')
    number = models.IntegerField()
    level = models.CharField(default='w', max_length=1, choices=LEVEL)
    teamone = ChainedForeignKey('league.team', middle='tournament.participant', related_name="matchup_team_one", chained_field='tournament', chained_model_field='tournament', show_all=False, blank=True, null=True)
    teamtwo = ChainedForeignKey('league.team', middle='tournament.participant', related_name="matchup_team_two", chained_field='tournament', chained_model_field='tournament', show_all=False, blank=True, null=True)
    teamonescore = models.IntegerField(default=0)
    teamtwoscore = models.IntegerField(default=0)
    date = models.DateField(default=lambda: datetime.now(), blank=True, null=True)
    tier = models.IntegerField()
    seedsto = models.ForeignKey('Matchup', related_name="seeds_to_winner", default=None, blank=True, null=True)
    seedsto_loser = models.ForeignKey('Matchup', related_name="seeds_to_loser", default=None, blank=True, null=True)
    winner = -1
    loser = -1

    def __unicode__(self):
        status = " #Unplayed#" if not self.has_winner() else ""

        if self.teamone is None:
            t1 = "Bye"
        else:
            t1 = self.teamone.short

        if self.teamtwo is None:
            t2 = "Bye"
        else:
            t2 = self.teamtwo.short

        return self.tournament.short + "-" + self.level + "." + str(self.tier) + "." + str(self.number) + " - " + t1 + " vs " + t2 + status

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

    class Meta:
        unique_together = ('tournament', 'tier', 'number', 'level')


class Participant(models.Model):
    tournament = models.ForeignKey('Tournament')
    team = models.ForeignKey(Team)
    seed = models.IntegerField(default=0)
    placement = models.IntegerField(default=0)

    def __unicode__(self):
        return self.tournament.name + "." + self.team.name

    class Meta:
        unique_together = ('tournament', 'team')


class Tournament(models.Model):
    TYPES = (
        ('s', 'Single Elimination'),
        ('d', 'Double Elimination'),
        ('r', 'Round Robin'),
    )

    name = models.CharField(max_length=30)
    short = models.CharField(max_length=30)
    flavor = models.TextField(default="")
    splash = models.FileField(upload_to="tournaments", default="tournaments/default.png")
    t_type = models.CharField(max_length=1, choices=TYPES, default='d')

    def randomize_seeds(self):
        #NYI
        None

    def generate(self):
        matchups = []
        if self.t_type == 'd' or self.t_type == 's':
            teams = list(Participant.objects.filter(tournament=self).order_by('seed'))
            num = len(teams)
            print "gen for " + str(num) + " teams"
            num_tierone = pow2roundup(int(ceil(num/2)))
            print "tier one matchups " + str(num_tierone)
            for i in range(num_tierone):
                matchup = Matchup()
                matchup.tournament = self
                if i < ceil(num/2):
                    matchup.teamone = teams[i].team
                else:
                    matchup.teamone = None
                if num-1-i > num//2:
                    matchup.teamtwo = teams[num-1-i].team
                else:
                    matchup.teamtwo = None
                matchup.tier = 0
                matchup.date = None
                matchup.number = (i)
                matchups.append(matchup)
                matchup.save()
                print "adding " + matchup.__unicode__()

            num_tier = num_tierone
            off = 0
            tier = 0
            while num_tier > 1:
                num_tier //= 2
                tier += 1
                for i in range(num_tier):
                    #print tier, i, off
                    next_matchup = Matchup()
                    next_matchup.tournament = self
                    next_matchup.tier = tier
                    next_matchup.date = None
                    next_matchup.number = (i)
                    next_matchup.save()
                    matchups[off + i * 2].seedsto = next_matchup
                    matchups[off + i * 2].save()
                    matchups[off + i * 2 + 1].seedsto = next_matchup
                    matchups[off + i * 2 + 1].save()
                    matchups.append(next_matchup)
                    print "adding " + next_matchup.__unicode__()

                off = len(matchups)-num_tier

        # Add loserbracket matches if double elim NYI
        """
        if self.t_type == 'd':
            num_tier = num_tierone
            off = 0
            tier = 0
            while num_tier > 1:
                num_tier //= 2
                tier += 1
                for i in range(num_tier):
                    #print tier, i, off
                    next_matchup = Matchup()
                    next_matchup.level = 'l'
                    next_matchup.tournament = self
                    next_matchup.tier = tier
                    next_matchup.date = None
                    next_matchup.number = (i)
                    next_matchup.save()
                    matchups[off + i * 2].seedsto_loser = next_matchup
                    matchups[off + i * 2].save()
                    matchups[off + i * 2 + 1].seedsto_loser = next_matchup
                    matchups[off + i * 2 + 1].save()
                    matchups.append(next_matchup)
                    print "adding " + next_matchup.__unicode__()

                off = len(matchups)-num_tier
        """

        # NYI round robin
        if self.t_type == 'r':
            None

    def __unicode__(self):
        return self.name
