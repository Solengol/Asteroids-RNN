import tensorflow as tf
from tensorflow import keras
import random
import numpy as np
from statistics import mean, median
from collections import Counter
from main import Game as game

def initial_population():
    training_data = []
    scores = []
    accepted_scores = []    
    for i in range(initial_games):
        print('Initial Population', ' Simulation: ', i + 1, '/' , initial_games)
        env.reset()
        score = 0
        game_memory = []
        prev_observation = []  
        for _ in range(goal_steps):
            action = [0, 0, 0, 0]
            for a in range(0, len(action)):
                action[a] = random.choice([0, 1])   
            observation, reward, done, info = env.run(action)
            if len(prev_observation) > 0:
                game_memory.append([prev_observation, action])
            prev_observation = observation
            score += reward
            if done:
                break
        if score >= score_requirement:
            accepted_scores.append(score)
            for data in game_memory:
                training_data.append(data)
        scores.append(score)
    training_data_save = np.array(training_data)
    training_data_name = 'data_gen_0.npy'
    np.save('data/' + training_data_name, training_data_save, allow_pickle=True)
    print('Initial Population', ' Number of accepted scores:', len(accepted_scores))
    print('Initial Population', ' Mean accepted score:', mean(accepted_scores))
    print('Initial Population', ' Median accepted score:', median(accepted_scores))

def recursive_learning(generation):
    training_data = np.load('data/data_gen_' + str(generation - 1) + '.npy', allow_pickle=True)
    model = train_model(training_data)
    model_name = 'model_gen_' + str(generation)
    model.save('models/' + model_name)
    training_data = []   
    scores = []
    accepted_scores = []
    for i in range(initial_games):
        print('Generation:', generation, ' Simulation: ', i + 1, '/' , initial_games)
        env.reset()
        score = 0
        game_memory = []
        prev_observation = []  
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
            if len(prev_observation) > 0:
                game_memory.append([new_observation, action])       
            score += reward
            if done:
                break
        if score >= score_requirement:
            accepted_scores.append(score)
            for data in game_memory:
                training_data.append(data)
        scores.append(score)
    training_data_save = np.array(training_data)
    training_data_name = 'data_gen_' + str(generation) + '.npy'
    np.save('data/' + training_data_name, training_data_save, allow_pickle=True)
    print('Generation:', generation, ' Number of accepted scores:', len(accepted_scores))
    print('Generation:', generation, ' Mean accepted score:', mean(accepted_scores))
    print('Generation:', generation, ' Median accepted score:', median(accepted_scores))

def neural_network_model(input_size):
    model = keras.Sequential([
    keras.layers.Dense(12, input_dim = input_size, activation = 'sigmoid'),
    keras.layers.Dense(12, activation = 'sigmoid'),
    keras.layers.Dense(4, activation='softmax'),
    keras.layers.Dropout(0.8)
    ])
    opt = keras.optimizers.Adam(learning_rate=LR)
    model.compile(optimizer=opt,
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=['accuracy'])
    model.summary()
    return model

def train_model(training_data, model=False):
    X = np.array([i[0] for i in training_data])
    
    y = np.array([i[1] for i in training_data])
    if not model:
          model = neural_network_model(input_size = len(X[0]))
    model.fit(X, y, epochs = 5)
    return model

if __name__ == "__main__":
    #training_data = initial_population()
    LR = 1e-3
    env = game()
    goal_steps = 1000
    score_requirement = 0
    initial_games = 100
    generations = 10

    initial_population()
    for g in range (1, generations + 1):
        recursive_learning(g)

