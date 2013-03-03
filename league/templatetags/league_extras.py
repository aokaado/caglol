from league.models import Team, Match
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def bold_team(teamname, team):
    if teamname == team.name:
        return mark_safe("<b>%s</b>" % teamname)
    return teamname


@register.filter
def decorate_score(match, team):
    score = str(match.teamonescore) + " - " + str(match.teamtwoscore)
    if match.has_winner():
        if match.winner.name == team.name:
            return mark_safe("<span class='label label-success'>%s</span>" % score)
        else:
            return mark_safe("<span class='label label-important'>%s</span>" % score)
    return mark_safe("<span class='label label-warning'>%s</span>" % score)
