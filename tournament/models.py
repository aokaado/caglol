from __future__ import division
from django.db import models
from math import ceil, log, pow
from league.models import Team
from datetime import datetime
from smart_selects.db_fields import ChainedForeignKey
from tournament.utils import pow2roundup
from random import shuffle


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
    tier = models.FloatField()
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

        return self.tournament.short + "-" + self.level.upper() + "-" + str(self.tier) + "-" + str(self.number) + " - " + t1 + " vs " + t2 + status

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

    def apply_results(self):
        if self.has_winner():
            if self.tier == self.tournament.tiers and self.winner == self.teamtwo and self.seedsto is None:
                # If this is the superfinal in a double elim, and loserbracket team won
                superfinal_2 = Matchup()
                superfinal_2.level = 'w'
                superfinal_2.tournament = self
                superfinal_2.tier = self.tier + 1
                superfinal_2.date = None
                superfinal_2.number = (0)
                superfinal_2.teamone = self.teamone
                superfinal_2.teamtwo = self.teamtwo
                superfinal_2.save()

                self.seedsto = superfinal_2
                self.seedsto_loser = superfinal_2
                self.save()

            if self.tier < self.tournament.tiers-1:

                if self.number % 2:
                    self.seedsto.teamtwo = self.winner
                else:
                    self.seedsto.teamone = self.winner
                self.seedsto.save()

                if self.tournament.t_type == 'd' and self.level == 'w':
                    if self.number % 2 and self.tier == 0:
                        self.seedsto_loser.teamtwo = self.loser
                    else:
                        self.seedsto_loser.teamone = self.loser
                    self.seedsto_loser.save()

                if self.tournament.t_type == 'd' and self.level == 'l':
                    self.seedsto.teamtwo = self.winner
                    self.seedsto.save()

                if (self.tournament.t_type == 'd' and self.level == 'l') or self.tournament.t_type == 's':
                    try:
                        p = Participant.objects.get(tournament=self.tournament, team=self.loser)
                        p.placement = pow(2, self.tournament.tiers - self.tier)  # TODO make accurate
                        p.save()
                    except:
                        None

    def save(self, *args, **kwargs):
        self.apply_results()
        super(Matchup, self).save(*args, **kwargs)

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
    tiers = models.IntegerField(default=0)
    generated = models.BooleanField(default=False)

    def randomize_seeds(self):
        teams = Participant.objects.filter(tournament=self)
        num = len(teams)
        seeds = range(num)
        shuffle(seeds)
        for team in teams:
            team.seed = seeds.pop()
            team.save()

    def generate(self):
        matchups = []
        if self.t_type == 'd' or self.t_type == 's':
            teams = list(Participant.objects.filter(tournament=self).order_by('seed'))
            num = len(teams)
            print "gen for " + str(num) + " teams"
            num_tierone = pow2roundup(int(ceil(num/2)))
            tiers = int(log(num_tierone, 2))+1
            print "tier one matchups " + str(num_tierone) + " in " + str(tiers) + " tiers "

            for i in range(num_tierone * 2 - num):
                teams.append(None)

            for i in range(num_tierone):
                matchup = Matchup()
                matchup.tournament = self
                if teams[i] is not None:
                    matchup.teamone = teams[i].team
                if teams[num_tierone*2-1-i] is not None:
                    matchup.teamtwo = teams[num_tierone*2-1-i].team
                matchup.tier = 0
                matchup.date = None
                matchup.number = (i)
                matchups.append(matchup)
                matchup.save()
                #print "adding " + matchup.__unicode__()

            print ""
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
                    #print "adding " + next_matchup.__unicode__()

                off = len(matchups)-num_tier
                print ""

        # Add loserbracket matches if double elim NYI
        if self.t_type == 'd':
            lmatchups = []
            for i in range(num_tierone//2):
                matchup = Matchup()
                matchup.tournament = self
                matchup.tier = 0
                matchup.date = None
                matchup.level = 'l'
                matchup.number = (i)
                matchup.save()
                matchups[i * 2].seedsto_loser = matchup
                matchups[i * 2].save()
                matchups[i * 2 + 1].seedsto_loser = matchup
                matchups[i * 2 + 1].save()
                lmatchups.append(matchup)
                #print "adding " + matchup.__unicode__()

            num_tier = num_tierone//2
            off = 0
            woff = 0
            tier = 1
            while num_tier > 1:
                losers = num_tier
                winners = int(pow(2, tiers-tier-1))
                #print "losers", losers, "winners", winners, "tier", tier
                if winners < losers:
                    midtier = losers//2
                    # print "midtier"
                    for i in range(midtier):

                        next_matchup = Matchup()
                        next_matchup.level = 'l'
                        next_matchup.tournament = self
                        next_matchup.tier = tier - 0.5
                        next_matchup.date = None
                        next_matchup.number = (i)
                        next_matchup.save()
                        lmatchups.append(next_matchup)

                        lmatchups[off + i * 2].seedsto = next_matchup
                        lmatchups[off + i * 2].save()

                        lmatchups[off + i * 2 + 1].seedsto = next_matchup
                        lmatchups[off + i * 2 + 1].save()

                        #print "adding " + str(len(lmatchups)-1) + " " + next_matchup.__unicode__()
                    num_tier = midtier

                else:
                    #print "mergetier"
                    mergetier = losers//2 + winners//2
                    for i in range(mergetier):
                        #print "merge", tier, num_tier, i, off

                        next_matchup = Matchup()
                        next_matchup.level = 'l'
                        next_matchup.tournament = self
                        next_matchup.tier = tier
                        next_matchup.date = None
                        next_matchup.number = (i)
                        next_matchup.save()
                        lmatchups.append(next_matchup)

                        matchups[num_tierone + woff + i].seedsto_loser = next_matchup
                        matchups[num_tierone + woff + i].save()

                        lmatchups[off + i].seedsto = next_matchup
                        lmatchups[off + i].save()

                        #print "adding " + str(len(lmatchups)-1) + " " + next_matchup.__unicode__()
                    woff += winners
                    tier += 1
                    num_tier = mergetier

                off = len(lmatchups)-num_tier

            superfinal = Matchup()
            superfinal.level = 'w'
            superfinal.tournament = self
            superfinal.tier = tier + 1
            superfinal.date = None
            superfinal.number = (0)
            superfinal.save()
            #print "adding superfinal " + superfinal.__unicode__()

            matchups[-1].seedsto = superfinal
            matchups[-1].seedsto_loser = lmatchups[-1]
            matchups[-1].save()
            lmatchups[-1].seedsto = superfinal
            lmatchups[-1].save()

            for m in lmatchups:
                if m.seedsto is None:
                    print "l miss", m
            for m in matchups:
                if m.seedsto is None:
                    print "w miss", m
                if m.seedsto_loser is None:
                    print "w-l miss", m

        # NYI round robin
        if self.t_type == 'r':
            None

        self.generated = True
        self.tiers = tiers
        self.save()

    def __unicode__(self):
        return self.name
