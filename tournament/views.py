from tournament.models import Tournament, Matchup
from django.shortcuts import render_to_response, get_object_or_404
from utils import create_tiered_list


def tournament(request, tournament_id=1):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    wm = list(Matchup.objects.filter(tournament=tournament_id, tier=0, level='w').order_by('level', 'tier', 'number'))
    wmatchups = create_tiered_list(wm)

    if tournament.t_type == 'd':
        lm = list(Matchup.objects.filter(tournament=tournament_id, tier=0, level='l').order_by('level', 'tier', 'number'))
        lmatchups = create_tiered_list(lm)
    else:
        lmatchups = None

    return render_to_response('tournament/tournament.html', {'tournament': tournament, 'wmatchups': wmatchups, 'lmatchups': lmatchups})


def tournaments(request):
    tournaments = Tournament.objects.filter(generated=True)
    return render_to_response('tournament/index.html', {'tournaments': tournaments})
