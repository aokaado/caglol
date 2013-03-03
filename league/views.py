from league.models import Player, Team, Match, League, Standings
from django.shortcuts import render_to_response
#import time


def league(request, league_id=1):
    league = League.objects.get(pk=league_id)
    standings = Standings.objects.filter(league=league_id).order_by('-score', '-wins', 'losses')
    #teams.sort(reverse=True)
    matches = Match.objects.filter(league=league).order_by('-date')[:8]
    return render_to_response('league/league.html', {'standings': standings, 'matches': matches, 'league': league})


def leagues(request):
    leagues = League.objects.all()
    return render_to_response('league/index.html', {'leagues': leagues})


def players(request, start=0):
    start = int(start)
    stride = 10
    players = Player.objects.all()[start*stride:start*stride + stride]
    return render_to_response('player/index.html', {'players': players, 'i': start})


def player(request, player_id):
    player = Player.objects.get(pk=player_id)
    return render_to_response('player/player.html', {'player': player})


def teams(request, start=0):
    start = int(start)
    stride = 10
    teams = Team.objects.all()[start*stride:start*stride + stride]

    return render_to_response('team/index.html', {'teams': teams, 'i': start})


def team(request, team_id):
    team = Team.objects.get(pk=team_id)
    players = team.player.all()
    matches = Match.objects.all().order_by('date')
    standings = Standings.objects.filter(team=team)
    matches2 = [m for m in matches if m.teamone.id == team.id or m.teamtwo.id == team.id]

    return render_to_response('team/team.html', {'team': team, 'players': players, 'matches': matches2, 'standings': standings})


def matches(request, start=0):
    start = int(start)
    stride = 10
    matches = Match.objects.all().order_by('date')[start*stride:start*stride + stride]

    return render_to_response('match/index.html', {'matches': matches})


def match(request, match_id):
    match = Match.objects.get(pk=match_id)

    return render_to_response('match/match.html', {'match': match})
