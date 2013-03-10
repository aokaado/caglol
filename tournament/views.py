from tournament.models import Tournament, Matchup
from django.shortcuts import render_to_response
from utils import create_tiered_list


def tournament(request, tournament_id=1):
    tournament = Tournament.objects.get(pk=tournament_id)
    wm = list(Matchup.objects.filter(tournament=tournament_id, tier=0, level='w').order_by('level', 'tier', 'number'))
    wmatchups = create_tiered_list(wm)

    if tournament.t_type == 'd':
        lm = list(Matchup.objects.filter(tournament=tournament_id, tier=0.5, level='l').order_by('level', 'tier', 'number'))
        lmatchups = create_tiered_list(lm)
    else:
        lmatchups = None

    return render_to_response('tournament/tournament.html', {'tournament': tournament, 'wmatchups': wmatchups, 'lmatchups': lmatchups})


def tournaments(request):
    tournaments = Tournament.objects.all()
    return render_to_response('tournament/index.html', {'tournaments': tournaments})
