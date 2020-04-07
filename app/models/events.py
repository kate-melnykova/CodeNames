from typing import List

from models.db import db
from models.models import Game


class Event:
    @classmethod
    def get_key(cls, game_id: str, name: str):
        return f'{game_id}:{name}'

    def __init__(self, event, game_id: str):
        game = Game.load(game_id)
        if game is None:
            raise

        for player in game.get_all_players():
            key = self.get_key(game_id, player.name)
            data = db.load(key)
            if data is None:
                data = list()
            data.append(event)
            db.save(key, data)

    @classmethod
    def get(cls, game_id: str, name: str) -> List['Event']:
        """
        gets the stored events given the key and erases them
        :param game_id: game_id of the game of interest
        :param name: name of the user
        :return: all events that happened
        """
        key = cls.get_key(game_id, name)
        data = db.load(key)
        if data is not None:
            db.delete(key)
            return data
        else:
            return list()
