from core.models import Game


def available_games(request):
    if request.user.is_authenticated:
        games = Game.objects.filter(player2=None, game_status='created').exclude(player1=request.user)
    else:
        games = Game.objects.filter(player2=None, game_status='created')
    return {'available_games': games}