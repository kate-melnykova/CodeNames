import json
from random import randint
from uuid import uuid4
from typing import List

from models.db import db


class User:
    def __init__(self, name: str, team=None, wants_codemaster=False, codemaster=False):
        self.name = name
        self.team = team
        self.codemaster = codemaster
        self.wants_codemaster = wants_codemaster


    def serialize(self):
        data = {
            'name': self.name,
            'team': self.team,
            'wants_codemaster': self.wants_codemaster,
            'codemaster': self.codemaster
        }
        return json.dumps(data)

    @classmethod
    def deserialize(cls, data):
        return cls(**json.loads(data))


class Game:
    n_rows = 5
    n_cols = 5
    n_entries = 25
    n_red = 8
    n_blue = 8

    def __init__(self, **kwargs):
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)

    @classmethod
    def create(cls):
        cards_selected = list()
        while len(cards_selected) < cls.n_entries:
            idx = randint(1, 278)
            if idx not in cards_selected:
                cards_selected.append(idx)

        start_color = randint(0, 1)
        if start_color:
            turn = 'b'
            n_red = cls.n_red
            n_blue = cls.n_blue + 1
        else:
            turn = 'r'
            n_red = cls.n_red + 1
            n_blue = cls.n_blue

        coloring = ['w'] * cls.n_entries
        coloring[randint(0, cls.n_entries - 1)] = 'b'
        while n_red > 0:
            idx = randint(0, cls.n_entries - 1)
            if coloring[idx] == 'w':
                coloring[idx] = 'r'
                n_red -= 1
        while n_blue > 0:
            idx = randint(0, cls.n_entries - 1)
            if coloring[idx] == 'w':
                coloring[idx] = 'b'
                n_blue -= 1

        self = cls(
            id=str(uuid4())[:4],
            _all_players=list(),
            state='waiting',
            cards_selected=cards_selected,
            turn=turn,
            coloring=coloring,
            revealed=list(),
            codemaster_red=None,
            codemaster_blue=None
        )
        self.save()
        return self

    @classmethod
    def load(cls, game_id: str) -> 'Game' or None:
        data = db.load(game_id)
        if data is None:
            return None

        data = json.loads(data)
        print(data)
        data['_all_players'] = [User.deserialize(d) for d in data['_all_players']]
        if data['codemaster_blue'] is not None:
            data['codemaster_blue'] = User.deserialize(data['codemaster_blue'])
        if data['codemaster_red'] is not None:
            data['codemaster_red'] = User.deserialize(data['codemaster_red'])
        return cls(**data)

    def save(self):
        data = dict()
        data['id'] = self.id
        data['_all_players'] = [player.serialize() for player in self._all_players]
        data['state'] = self.state
        data['cards_selected'] = self.cards_selected
        data['turn'] = self.turn
        data['coloring'] = self.coloring
        data['revealed'] = self.revealed
        data['codemaster_red'] = self.codemaster_red.serialize() if self.codemaster_red is not None else None
        data['codemaster_blue'] = self.codemaster_blue.serialize() if self.codemaster_blue is not None else None
        print(data)
        data = json.dumps(data)
        db.save(self.id, data)

    def get_player(self, name: str) -> 'User' or None:
        for player in self.get_all_players():
            if player.name == name:
                return player

        return None

    def get_all_players(self) -> List['User']:
        return list(self._all_players)

    def add_player(self, name: str, wants_codemaster: bool):
        user = User(name, wants_codemaster=wants_codemaster)
        self._all_players.append(user)

