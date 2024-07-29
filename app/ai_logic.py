from collections import Counter
import random
import numpy as np
from app.models import GameRound
from app import db


class RockPaperScissorsAI:
    def __init__(self):
        self.choices = ['rock', 'paper', 'scissors']
        self.model_scores = [0] * 4
        self.game_history = []
        
        # Load pre-trained ML models
        # with open('neural_network_model.pkl', 'rb') as f:
        #     self.nn_model = pickle.load(f)
        # with open('decision_tree_model.pkl', 'rb') as f:
        #     self.dt_model = pickle.load(f)

    def get_winning_move(self, choice):
        return self.choices[(self.choices.index(choice) + 1) % 3]

    def get_losing_move(self, choice):
        return self.choices[(self.choices.index(choice) - 1) % 3]

    def model_0(self, player_history):
        if len(player_history) < 3:
            return random.choice(self.choices)
        
        # Check if player is changing their answers in the past three rounds
        changing = len(set(player_history[-3:])) > 1
        
        if changing:
            return self.get_losing_move(player_history[-1])
        else:
            return self.get_winning_move(player_history[-1])

    def model_1(self, player_history):
        if len(player_history) < 3:
            return random.choice(self.choices)
        
        pattern = ''.join([c[0] for c in player_history[-3:]])
        next_move = {'rps': 'r', 'psr': 'p', 'srp': 's',
                     'rpr': 'p', 'psp': 's', 'srs': 'r',
                     'rsr': 's', 'prs': 'r', 'sps': 'p'}.get(pattern, random.choice(self.choices))
        return self.get_winning_move(next_move)

    def model_2(self, player_history):
        if not player_history:
            return random.choice(self.choices)
        most_common = Counter(player_history).most_common(1)[0][0]
        return self.get_winning_move(most_common)

    def model_3(self, player_history):
        if not player_history:
            return random.choice(self.choices)
        
        choice_counts = Counter(player_history)
        
        if len(set(choice_counts.values())) == 1:
            return random.choice(self.choices)
        
        least_common = min(choice_counts, key=choice_counts.get)
        return self.get_winning_move(least_common)

    def model_4(self, game_history):
        if len(game_history) < 7:
            return random.choice(self.choices)
        input_data = self.prepare_input_data(game_history[-7:])
        prediction = self.nn_model.predict(input_data)[0]
        return self.get_winning_move(self.choices[prediction])

    def model_5(self, game_history):
        if len(game_history) < 5:
            return random.choice(self.choices)
        input_data = self.prepare_input_data(game_history[-5:])
        prediction = self.dt_model.predict(input_data)[0]
        return self.get_winning_move(self.choices[prediction])

    def prepare_input_data(self, history):
        # Convert game history to numerical format for ML models
        # This is a placeholder and should be adjusted based on your actual input format
        return np.array([[self.choices.index(round['player_choice']) for round in history]])

    def update_model_scores(self, winner):
        n = len(self.game_history)
        for i in range(len(self.model_scores)):
            score = 0
            denominator = 0
            for j in range(1, n + 1):
                if self.game_history[-j]['model_used'] == i:
                    if winner == 'computer':
                        a_j = 1
                    elif winner == 'player':
                        a_j = -1
                    else:  # tie
                        a_j = 0
                    score += a_j * j * j
                denominator += j * j
            self.model_scores[i] = score / denominator if denominator != 0 else 0

    def choose_model(self):
        return self.model_scores.index(max(self.model_scores))

    def make_choice(self, player_history):
        model_index = self.choose_model()
        models = [self.model_0, self.model_1, self.model_2, self.model_3, self.model_4, self.model_5]
        return models[model_index](player_history)

    def play_round(self, player_choice):
        ai_choice = self.make_choice([round['player_choice'] for round in self.game_history])
        
        if player_choice == ai_choice:
            winner = 'tie'
        elif (self.choices.index(player_choice) - self.choices.index(ai_choice)) % 3 == 1:
            winner = 'player'
        else:
            winner = 'computer'

        self.game_history.append({
            'player_choice': player_choice,
            'ai_choice': ai_choice,
            'winner': winner,
            'model_used': self.choose_model()
        })

        self.update_model_scores(winner)
        return ai_choice, winner
