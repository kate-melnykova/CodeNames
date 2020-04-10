import time
from random import randint, shuffle

from flask import Flask, render_template, redirect, request, flash, url_for, \
    make_response, jsonify

from models.models import Game
from models.wtforms import CreateGameForm
from models.events import Event

app = Flask(__name__)
app.secret_key = '12mkljijalkkfmqa4543gwrg'
app.config.from_object('config')


def get_game():
    game_id = request.cookies.get(app.config['COOKIE_GAME_ID'])
    # load game with given game_id
    return Game.load(game_id)


def get_user(game):
    name = request.cookies.get(app.config['COOKIE_USER_ID'])
    return game.get_player(name)


def get_event(game_id: str, name: str):
    return Event.get(game_id, name)


@app.route('/')
def main():
    form = CreateGameForm()
    return render_template('main.html', form=form)


@app.route('/setup', methods=['POST'])
def setup():
    form = CreateGameForm(request.form)
    # create or load the game
    if not form.join.data:
        # create a new game
        game = Game.create()
    else:
        code = form.join.data
        game = Game.load(code)
        if game is None:
            flash('Incorrect game id')
            return redirect(url_for('main'))

    print(f'Want to be codemaster: {form.codemaster.data}')
    game.add_player(form.name.data, form.codemaster.data)
    game.save()
    r = make_response(redirect(url_for('waiting')))
    r.set_cookie(app.config['COOKIE_USER_ID'], form.name.data)
    r.set_cookie(app.config['COOKIE_GAME_ID'], game.id)
    return r


@app.route('/waiting', methods=['GET', 'POST'])
def waiting():
    game = get_game()
    user = get_user(game)
    if game is None:
        flash('No game with such id')
        return redirect(url_for('main'))

    if request.method == 'GET':
        if game.state != 'waiting':
            # TODO if person is not `colored`, color them
            return redirect(url_for('play'))
        elif 'start' in request.args:
            print('I am here')
            all_players = game.get_all_players()
            maybe_codemaster = [p for p in all_players if p.wants_codemaster]
            # select red codemaster
            if maybe_codemaster:
                i = randint(0, len(maybe_codemaster) - 1)
                game.codemaster_red = maybe_codemaster.pop(i)
                all_players.remove(game.codemaster_red)
            else:
                i = randint(0, len(all_players) - 1)
                game.codemaster_red = all_players.pop(i)
            game.codemaster_red.codemaster = True
            game.codemaster_red.team = 'red'
            print(f'Codemaster red is {game.codemaster_red.name}')

            # select codemaster blue
            if maybe_codemaster:
                i = randint(0, len(maybe_codemaster) - 1)
                game.codemaster_blue = maybe_codemaster.pop(i)
                all_players.remove(game.codemaster_blue)
            else:
                i = randint(0, len(all_players) - 1)
                game.codemaster_blue = all_players.pop(i)
            game.codemaster_blue.codemaster = True
            game.codemaster_blue.team = 'blue'
            print(f'Codemaster blue is {game.codemaster_blue.name}')

            shuffle(all_players)
            length = len(all_players)
            i = 0
            while i < length:
                all_players[i].team = 'red' if i < length // 2 else 'blue'
                i += 1

            game._all_players = all_players
            game.state = 'play'
            game.save()
            return redirect(url_for('play'))
        else:
            return render_template('waiting.html', game=game, name=user.name)

    # request.method = 'POST'
    if game is None:
        url = url_for('main')
        users = []
    elif game.state == 'play':
        url = url_for('play')
        users = []
    else:
        url = None
        users = [p.name for p in game.get_all_players()]
    return jsonify({'url': url, 'users': users})

"""
@app.route('/play', methods=['POST'])
def start_game():
    if request.cookies.get('codenames_game_id') not in all_games:
        return redirect(url_for('main'))
    game = all_games[request.cookies.get('codenames_game_id')]
    if not game.status:
        game.start()

    return redirect(url_for('play'))
"""


@app.route('/play')
def play():
    game = get_game()
    user = get_user(game)
    if not game:
        flash('This game does not exist')
        return redirect(url_for('main'))

    if request.method == 'GET':
        return render_template('play.html', game=game, user=user)

    # request.method == 'POST'
    # TODO
    return render_template('play.html', game=game, user=user)


@app.route('/long_polling')
def long_polling():
    game = get_game()
    if game is None:
        return redirect(url_for('main'))

    player = get_user(game)
    while True:
        event = Event.get(game.id, player.name)
        if event:
            return jsonify(event)
        time.sleep(1)




