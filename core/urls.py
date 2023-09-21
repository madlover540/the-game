from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    # path('profile/', views.CreateUserProfile.as_view(), name='profile'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('find-game/', views.GameFindMatchView.as_view(), name='home'),
    path('waiting_room/', views.WaitingRoomView.as_view(), name='waiting-room'),
    path('high_scores/', views.HighScoresView.as_view(), name='high-scores'),
    path('start-game/', views.CreateGameView.as_view(), name='start-game'),
    path('start-game/<int:game_id>/', views.StartGameView.as_view(), name='join-game-id'),
    path('join-game/', views.JoinGameView.as_view(), name='join-game'),
    path('join-game/<int:game_id>/', views.JoinGameView.as_view(), name='join-game-pk'),
    path('', views.LandingGameLobby.as_view(), name='home'),
    path('about-us/', views.AboutUsView.as_view(), name='about-us'),
    path('contact-us/', views.ContactUsView.as_view(), name='contact-us'),
]