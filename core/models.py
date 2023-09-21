from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User
from model_utils import Choices
# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    numberofgames = models.IntegerField()
    highestscore = models.IntegerField()

    def __str__(self):
        return self.name



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    is_waiting_for_match = models.BooleanField(default=False)
    # ... any other user-related fields





class Game(models.Model):
    GAME_STATUS = Choices(
        ('started', 'GAME STARTED'),
        ('waiting', 'WAITING'),
        ('created', 'CREATED'),  # PARTIALLY_CAPTURED orders are also marked with this
        ('finished', 'FINISHED'),
       )
    player1 = models.ForeignKey(User, related_name='player1_games', on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name='player2_games', on_delete=models.CASCADE, null=True, blank=True, )
    current_turn = models.ForeignKey(User, related_name='current_turn_games', on_delete=models.CASCADE)
    number_to_guess = models.IntegerField()
    player1_score = models.IntegerField(default=0)
    player2_score = models.IntegerField(default=0)
    game_over = models.BooleanField(default=False)
    game_status = models.CharField(
        choices=GAME_STATUS,
        default=GAME_STATUS.created,
        max_length=30,
    )
    score = models.CharField(max_length=20, null=True, blank=True)
    winner = models.ForeignKey(User, related_name='the_winner', on_delete=models.CASCADE, null=True, blank=True)
    game_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.player2:
            return f'{self.player1.username} vs {self.player2.username}'
        return f'{self.player1.username} waiting..'


    def available_games(self):
        return Game.objects.filter(player1__userprofile__is_waiting_for_match=True, player1__userprofile__is_online=True, player2=None)
