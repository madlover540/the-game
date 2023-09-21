import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.shortcuts import get_object_or_404

from core.models import UserProfile, Game


class GameMatchingConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_avaialble_game_id(self):
        return Game.available_games

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass
        # Disconnect logic here, e.g., mark player as offline or leave a group.

    # This gets called when you receive a message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        game_id = text_data_json['game_id']

        if action == "wiating":
            # Your logic to match the player
            match_id = self.get_avaialble_game_id()
            print(match_id)

            if match_id:
                # Send a message to the player to start the game.
                await self.send(text_data=json.dumps({
                    'action': 'join_game',
                    'game_id': game_id
                }))
        elif action == 'start_game':
            await self.send(text_data=json.dumps({
                'action': 'start_game',
                'game_id': game_id
            }))

        elif action == "turn_end":
            await self.handle_turn_end(game_id)

            # Your logic to handle the end of the player's turn and notify player two
            await self.notify_player_two(game_id)

    @database_sync_to_async
    def handle_turn_end(self, game_id):
        game = get_object_or_404(Game, id=game_id)

        # Here, you'd get the user from the session or another method you've implemented.
        # If you're using Django's authentication, `self.scope["user"]` might work.
        current_user = self.scope.get("user")

        if current_user == game.player1:
            game.current_turn = game.player2
        elif current_user == game.player2:
            game.current_turn = game.player1

        game.save()
        print(game.current_turn)

        # NOTE: This would be a synchronous call; you might have to make it asynchronous as well if it deals with the database or other async code.
        self.notify_player_two(game_id)

    async def notify_player_two(self, game_id):
        # Logic to send a WebSocket message to player2
        # For simplicity, assuming that you have a mechanism to get player2's channel_name
        await self.send(text_data=json.dumps({
            'action': 'turn_notification',
            'message': 'Your turn',
            'game_id': game_id
        }))


    # def your_matching_function(self):
    #     # Get all users who are currently waiting for a match.
    #     waiting_players = self.get_waiting_players_count()
    #
    #     # If there are at least 2 players waiting for a match.
    #     ready_to_match = waiting_players
    #     if (len(waiting_players)) >= 2:
    #         player1 = waiting_players[0]
    #         player2 = waiting_players[1]
    #
    #         # Update their statuses so they are no longer waiting.
    #         player1.is_waiting_for_match = False
    #         player1.save()
    #
    #         player2.is_waiting_for_match = False
    #         player2.save()
    #
    #         # Create a new game instance with these two players.
    #         new_game = Game.objects.create(player1=player1, player2=player2)
    #
    #         # Return the game instance, indicating a match was found.
    #         return new_game
    #
    #     # If there's less than 2 players waiting, return None indicating no match.
    #     return None
