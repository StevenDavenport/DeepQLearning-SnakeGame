import os
import random
from keras.optimizer_v2 import adam
import numpy as np
from collections import deque
from itertools import count
import time

from keras.models import Model, load_model, Sequential 
from keras.layers import Input, Dense
from keras.optimizers import adam_v2
import matplotlib
import matplotlib.pyplot as plt


class Brain:
    def __init__(self):
        self.num_actions = 3
        self.num_observations = 4
        self.memory = deque(maxlen=2000)
        self.learning_rate = 1e-4
        self.epsilon = 1.0
        self.epsilon_min = 0.001
        self.gamma = 0.95
        self.batch_size = 64
        self.train_start = 1000
        self.steps_taken = 0
        self.update_target = 20
        self.moving_avg_period = 25
        self.moving_avg = []
        self.episode_rewards = []
        self.model = self.build_model()
        self.target_model = self.build_model()
        self.score_save_limit = 500
        self.epsilon_decay = 0.999

    def build_model(self):
        model = Sequential()
        model.add(Dense(512, input_dim=self.num_observations, activation="relu", kernel_initializer='he_uniform'))
        model.add(Dense(256, activation="relu", kernel_initializer='he_uniform'))
        model.add(Dense(64, activation="relu", kernel_initializer='he_uniform'))
        model.add(Dense(self.num_actions, activation="linear", kernel_initializer='he_uniform'))
        model.compile(loss="mse", optimizer=adam.Adam(learning_rate=self.learning_rate), metrics=["accuracy"])
        return model

    def take_action(self):
        if self.model == None:
            self.model = self.load_model('model/model.h5')
        state = np.squeeze(state).reshape(1,4)
        return np.argmax(self.model.predict(state))

    def plot(self):
        plt.figure(1)
        plt.clf()        
        plt.title('Training...')
        plt.xlabel('Episode')
        plt.ylabel('Duration')
        self.moving_avg.append(sum(self.episode_rewards[-self.moving_avg_period:]) // self.moving_avg_period if len(self.episode_rewards) >= self.moving_avg_period else 0)
        plt.plot(self.episode_rewards)
        plt.plot(self.moving_avg)    
        plt.pause(0.001)
    
    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def save_model(self, step):
        self.model.save('model' + str(step) + '.h5')