from flask import Flask, request, jsonify
import random
from collections import Counter
import numpy as np
#from sklearn.tree import DecisionTreeClassifier
#from sklearn.neural_network import MLPClassifier
import pickle

app = Flask(__name__)


# Initialize the AI
ai = RockPaperScissorsAI()


@app.route('/reset', methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True)