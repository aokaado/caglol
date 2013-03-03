from django.contrib import admin
from league.models import Player, Team, Match, League, Standings


def update_standing(modeladmin, request, queryset):
    for standing in queryset:
        standing.update()
update_standing.short_description = "Force update wins and losses"


class StandingsAdmin(admin.ModelAdmin):
    readonly_fields = ('wins', 'losses', 'score')
    actions = [update_standing]

admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(League)
admin.site.register(Standings, StandingsAdmin)
