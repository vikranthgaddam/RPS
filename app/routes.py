from datetime import datetime, timedelta
import random
from flask import Blueprint, request, jsonify
from app import db
from app.models import GameRound
from app.ai_logic import RockPaperScissorsAI
from app.aws_util import send_data_to_aws

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

@bp.route('/test_aws_send', methods=['GET'])
def test_aws_send():
    # Clear existing data
    db.session.query(GameRound).delete()
    db.session.commit()

    # Create sample data
    choices = ['rock', 'paper', 'scissors']
    winners = ['player', 'ai', 'tie']
    start_time = datetime.now() - timedelta(minutes=30)

    for i in range(20):  # Create 20 sample rounds
        round = GameRound(
            player_choice=random.choice(choices),
            ai_choice=random.choice(choices),
            winner=random.choice(winners),
            model_used=random.randint(0, 3),
            timestamp=start_time + timedelta(minutes=i)
        )
        db.session.add(round)

    db.session.commit()

    # Fetch all rounds and send to AWS
    rounds = GameRound.query.all()
    print("Rounds",rounds)
    success = send_data_to_aws(rounds, '127.0.0.1')  # Using a dummy IP address

    if success:
        return jsonify({'message': 'Sample data sent to AWS successfully'}), 200
    else:
        return jsonify({'message': 'Error sending sample data to AWS'}), 500

@bp.route('/reset', methods=['POST'])
def reset_game():
    global ai
    ai = RockPaperScissorsAI()
    return jsonify({'message': 'Game reset successfully'})
