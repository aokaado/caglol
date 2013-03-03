from league.models import Team
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def bold_team(teamname, team):
    if teamname == team.name:
        return mark_safe("<b>%s</b>" % teamname)
    return teamname

