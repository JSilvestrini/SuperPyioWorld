import environment
import torch
import random
import sys
import numpy as np
from collections import deque
from model import Network, QTrainer

MAX_MEMORY = 10000
BATCH_SIZE = 256
LEARNING_RATE = 0.001

class Agent:
    def __init__(self, device):
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        self.number_games = 0
        self.epsilon = 80
        self.gamma = 0.90
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Network().to(self.device)
        self.trainer = QTrainer(self.model, LEARNING_RATE, self.gamma, self.device)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state : torch.Tensor, action, reward, next_state, done):
        # done is going to be reverse
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        self.epsilon = 80 - self.number_games
        potential_move = np.zeros(16, dtype=np.int8)
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 15)
            potential_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype = torch.float).to(self.device)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            potential_move[move] = 1
        return potential_move

def train(n):
    agent = Agent(device='cuda')
    game = environment.Environment(device='cuda')

    while agent.number_games < n:
        state_old = game.state()
        move = agent.get_action(state_old)

        state_new, reward, dead = game.step(move)

        agent.train_short_memory(state_old, move, reward, state_new, dead)
        agent.remember(state_old, move, reward, state_new, dead)

        if dead:
            agent.number_games += 1
            agent.train_long_memory()
            if agent.number_games % 100 == 0:
                agent.model.save()
            game.reset()
            

if __name__ == "__main__":
    n_train = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    train(n_train)