import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.shortcuts import get_object_or_404
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from core.models import UserProfile, Game


class GameMatchingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'game_id'):
            # Remove from the game's group when disconnected
            await self.channel_layer.group_discard(
                self.game_group_name(),
                self.channel_name
            )

    @database_sync_to_async
    def get_available_game_id(self):
        game = Game.objects.filter(status="available").first()
        return game.id if game else None

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            action = text_data_json['action']
            game_id = text_data_json['game_id']
            self.game_id = game_id
            print('channel_name=', self.channel_name)

            if action == "waiting":
                # match_id = await self.get_avaialble_game_id()
                if game_id:
                    # Player One is already waiting; this player becomes Player Two.
                    await self.channel_layer.group_add(
                        self.game_group_name(),
                        self.channel_name
                    )
                    # Inform Player One it's their turn
                    await self.channel_layer.group_send(
                        f"game_{game_id}",
                        {
                            'type': 'game.message',
                            'action': 'turn_notification',
                            'next_turn': 'player1',
                            'game_id': game_id
                        }
                    )
                    # Inform this player they are Player Two and wait for their turn
                    await self.send(text_data=json.dumps({
                        'action': 'wait_for_opponent',
                        'next_turn': 'player2',
                        'game_id': game_id
                    }))
            elif action == 'start_game':
                await self.channel_layer.group_add(
                    self.game_group_name(),
                    self.channel_name
                )
                await self.channel_layer.group_send(
                    self.game_group_name(), {
                    'type': 'game.message',
                    'action': 'start_game',
                    'game_id': game_id
                })

            elif action == "turn_end":
                await self.handle_turn_end(game_id)
                await self.notify_next_turn(game_id)
        except json.JSONDecodeError:
            print("Invalid JSON received.")

    async def notify_next_turn(self, game_id):
        await self.channel_layer.group_send(
            self.game_group_name(),
            {
                'type': 'game_message',
                'action': 'turn_notification',
                'message': 'Your turn',
                'game_id': game_id
            }
        )

    async def game_message(self, event):
        await self.send(text_data=json.dumps(event))

    def game_group_name(self):
        return f"game_{self.game_id}"

    @database_sync_to_async
    def _sync_handle_turn_end(self, game_id):
        game = get_object_or_404(Game, id=game_id)
        current_user = self.scope.get("user")

        if current_user == game.player1:
            game.current_turn = game.player2
        elif current_user == game.player2:
            game.current_turn = game.player1

        game.save()
        print(game.current_turn)
        return game_id

    async def handle_turn_end(self, game_id):
        await self._sync_handle_turn_end(game_id)
        await self.notify_player_two(game_id)

    @database_sync_to_async
    def handle_game_end(self, game_id):
        game = get_object_or_404(Game, id=game_id)
        game.game_status = 'finished'
        game.save()

    async def notify_player_two(self, game_id):
        await self.send(text_data=json.dumps({
            'action': 'turn_notification',
            'message': 'Your turn',
            'game_id': game_id
        }))
