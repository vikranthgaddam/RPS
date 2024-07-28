from flask import Blueprint, request, jsonify
from app import db
from app.models import GameRound
from app.ai_logic import RockPaperScissorsAI
from app.aws_utils import send_data_to_aws

bp = Blueprint('main', __name__)

ai = RockPaperScissorsAI()

@bp.route('/play', methods=['POST'])
def play_round():
    data = request.json
    player_choice = data.get('choice')

    if player_choice not in ai.choices:
        return jsonify({'error': 'Invalid choice. Please choose rock, paper, or scissors.'}), 400

    ai_choice, winner = ai.play_round(player_choice)

    response = {
        'player_choice': player_choice,
        'ai_choice': ai_choice,
        'result': winner,
        'game_history': ai.game_history
    }

    return jsonify(response)

@bp.route('/end_game', methods=['POST'])
def end_game():
    # Your end_game logic here
    send_data_to_aws(GameRound.query.all(), request.remote_addr)

@bp.route('/reset', methods=['POST'])
def reset_game():
    global ai
    ai = RockPaperScissorsAI()
    return jsonify({'message': 'Game reset successfully'})
