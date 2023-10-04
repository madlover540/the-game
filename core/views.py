from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views import View
# Create your views here.
from .models import Game, UserProfile, Profile
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from core.forms import UserCreationForm


class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('core:login')
    template_name = 'core/register.html'



class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        # This is called when the user successfully logs in
        response = super().form_valid(form)  # Call the parent class's method

        # Your custom logic
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        profile.is_online = True
        profile.save()

        return response  #


class CustomLogoutView(LogoutView):
    template_name = 'core/logout.html'

class LandingGameLobby(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'core/game_lobby.html')


class CreateGameView(View):
    def get(self, request, *args, **kwargs):
        game = Game.objects.create(player1=request.user, player2=None, current_turn=request.user,
                                   number_to_guess=20)
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.is_waiting_for_match = True
        user_profile.save()

        return render(request, 'core/waiting_room.html', {'game_id': game.id, 'player_type': 'creator'})




class GameFindMatchView(View):
    def get(self, request, *args, **kwargs):
        waiting_players = UserProfile.objects.filter(is_online=True, ).exclude(user=request.user).values_list('pk', flat=True)
        available_games = Game.objects.filter(player1_id__in=waiting_players, player2=None)

        if not available_games:
            game = Game.objects.create(player1=request.user, player2=None, current_turn=request.user,
                                       number_to_guess=20)
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.is_waiting_for_match = True
            user_profile.save()
            return render(request, 'core/waiting_room.html', {'game_id': game.id, 'player_type': 'creator'})
        game_id = available_games.first().pk
        return render(request, 'core/landing_page.html',{'game_id': game_id, 'player_type': 'joiner'})



class WaitingRoomView(View):
    def get(self, request, *args, **kwargs):


        return render(request, 'core/waiting_room.html')
        # Find an online user who is waiting for a game
    def post(self, request, *args, **kwargs):
        room_number = request.POST.get('room_number')
        game = get_object_or_404(Game, id=room_number)
        if game:
            return render(request, 'core/start_game.html', {'game_id': room_number})




class HighScoresView(View):
    def get(self, request, *args, **kwargs):
        top_scores = Profile.objects.order_by('-highestscore')[:10]
        context = {'scores': top_scores}

        return render(request, 'core/high_scores.html', context)


class StartGameView(View):
    def get(self, request, *args, **kwargs):
        game_id = kwargs.get('game_id', None)
        if game_id:
            try:
                game = get_object_or_404(Game, pk=game_id)
                if game:
                    if game.game_status != "finished" and game.player1 == request.user:
                        if game.player2:
                            return render(request, 'core/start_game.html', {'game_id': game.id, 'player_type': 'Joiner'})
                        return render(request, 'core/waiting_room.html', {'game_id': game.id, 'player_type': 'Creator'})
                    elif game.game_status != "finished" and game.player2 == request.user:
                        return render(request, 'core/start_game.html', {'game_id': game.id, 'player_type': 'Joiner'})
                    elif game.player2:
                        messages.warning(request, "this game already started")
                        return render(request, 'core/join_game.html')

                    game.player2 = request.user
                    game.game_status = Game.GAME_STATUS.started
                    game.save()
                    return render(request, 'core/start_game.html', {'game_id': game.id})
                # Logic to join the game using game_id
                # If joined successfully, redirect to the game room or appropriate page
                messages.warning(request, "wrong game id")
                return render(request, 'core/join_game.html')
            except Exception as e:
                messages.warning(request, e)
                return render(request, 'core/join_game.html')

        game = Game.objects.filter(player1=request.user, player2=None).first()
        if not game:
            game = Game.objects.create(player1=request.user, player2=None, current_turn=request.user,
                                       number_to_guess=20)
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.is_waiting_for_match = True
            user_profile.save()
        return render(request, 'core/waiting_room.html', {'game_id': game.id, 'player_type': 'creator'})


class JoinGameView(View):
    def get(self, request, *args, **kwargs):

        return render(request, 'core/join_game.html')
    def post(self, request, *args, **kwargs):
        # game_id = kwargs['game_id']
        game_id = request.POST.get('game_id')
        try:
            game = get_object_or_404(Game, pk=game_id)
            is_current_player = request.user in [game.player1, game.player2]
            if game.game_status != 'finished' and (is_current_player or game.player2 is None):

                if not game.player2:
                    game.player2 = request.user
                    game.game_status = Game.GAME_STATUS.started
                    game.save()
                if game.player2 == request.user:
                    return render(request, 'core/waiting_room.html', {'game_id': game.id, 'player_type': 'joiner'})
                return render(request, 'core/waiting_room.html', {'game_id': game.id, 'player_type': 'creator'})
            # Logic to join the game using game_id
            # If joined successfully, redirect to the game room or appropriate page
            messages.warning(request, "wrong game id")
            return render(request, 'core/join_game.html')
        except Exception as e:
            messages.warning(request, e)
            return render(request, 'core/join_game.html')

class AboutUsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "core/about_us.html")


class ContactUsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "core/contact_us.html")