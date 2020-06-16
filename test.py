import random
import numpy as np
import tensorflow as tf
from main import Game as game
from tensorflow import keras


env = game()
env.reset()
goal_steps = 1000
prev_observation = []
model = keras.models.load_model('models/model_gen_8')

for _ in range(goal_steps):
    action = [0, 0, 0, 0]
    if len(prev_observation) == 0:
        for a in range(0, len(action)):
            action[a] = random.choice([0, 1])
    else:
        pred = np.argmax(model.predict(prev_observation))
        action[pred] = 1     
    new_observation, reward, done, info = env.run(action)
    prev_observation = np.array([new_observation])
    env.draw()
    if done:
        break