from tournament.models import Tournament, Matchup
from django.shortcuts import render_to_response


def tournament(request, tournament_id=1):
    tournament = Tournament.objects.get(pk=tournament_id)
    wmatchups = []
    wm2 = []
    wm = list(Matchup.objects.filter(tournament=tournament_id, tier=0, level='w').order_by('level', 'tier', 'number'))
    while (len(wm) > 0):
        m = wm.pop(0)
        if m in wm2:
            continue
        if m.seedsto is not None:
            wm.append(m.seedsto)
        wm2.append(m)

    ctier = 0
    arr = []
    while(len(wm2) > 0):
        m = wm2.pop(0)
        if not m.tier == ctier:
            ctier += 1
            wmatchups.append(arr)
            arr = []
        arr.append(m)
    ctier += 1
    wmatchups.append(arr)

    print ctier
    if tournament.t_type == 'd':
        lmatchups = Matchup.objects.filter(tournament=tournament_id, tier=0, level='l').order_by('level', 'tier', 'number')
    else:
        lmatchups = None

    return render_to_response('tournament/tournament.html', {'tournament': tournament, 'wmatchups': wmatchups, 'lmatchups': lmatchups})


def tournaments(request):
    tournaments = Tournament.objects.all()
    return render_to_response('tournament/index.html', {'tournaments': tournaments})
