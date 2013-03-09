from django.contrib import admin
from tournament.models import Tournament, Matchup, Participant

admin.site.register(Tournament)
admin.site.register(Participant)
admin.site.register(Matchup)
