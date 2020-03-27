from flask import Flask, render_template, redirect, request, flash, url_for, \
    make_response

from models import Game
from models.wtforms import CreateGameForm

app = Flask(__name__)
app.secret_key='12mkljijalkkfmqa4543gwrg'
all_games = dict()


@app.route('/')
def main():
    form = CreateGameForm()
    return render_template('main.html', form=form)


@app.route('/setup', methods=['POST'])
def setup():
    form = CreateGameForm(request.form)
    if not form.join.data:
        # create a new game
        game = Game()
        all_games[game.id] = game
    else:
        code = form.join.data
        if code not in all_games:
            flash('Incorrect code')
            return redirect(url_for('main'))

        else:
            game = all_games[code]

    game.add_player(form.name.data, form.codemaster.data)
    r = make_response(redirect(url_for('waiting')))
    r.set_cookie('codenames_name', form.name.data)
    r.set_cookie('codenames_game_id', game.id)
    return r


@app.route('/waiting')
def waiting():
    if request.cookies.get('codenames_game_id') not in all_games:
        flash('No game with such id')
        print(f'No game with such id={request.cookies.get("codenames_game_id")}', all_games)
        return redirect(url_for('main'))

    game = all_games[request.cookies.get('codenames_game_id')]
    if game.status:
        return redirect(url_for('play'))
    else:
        return render_template('waiting.html', players=game.all_users)


@app.route('/start_game', methods=['POST'])
def start_game():
    if request.cookies.get('codenames_game_id') not in all_games:
        return redirect(url_for('main'))
    game = all_games[request.cookies.get('codenames_game_id')]
    if not game.status:
        game.start()

    return redirect(url_for('play'))


@app.route('/play')
def play():
    if request.cookies.get('codenames_game_id') not in all_games:
        return redirect(url_for('main'))
    game = all_games[request.cookies.get('codenames_game_id')]
    return render_template('play.html', game=game, name=request.cookies.get('name'))




