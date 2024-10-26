import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class Network(nn.Module):
    def __init__(self):
        super(Network, self).__init__()
        self.cnn1 = nn.Conv2d(3, 12, 25)
        self.cnn2 = nn.Conv2d(12, 24, 25)
        self.lnn1 = nn.Linear(221088, 256)
        self.lnn2 = nn.Linear(256, 64)
        self.lnn3 = nn.Linear(64, 16)

    def forward(self, input):
        c1 = F.relu(self.cnn1(input))
        s2 = F.max_pool2d(c1, (2, 2))
        c2 = F.relu(self.cnn2(s2))
        s3 = F.max_pool2d(c2, 2)
        s3 = torch.flatten(s3, 1)
        l1 = F.relu(self.lnn1(s3))
        l2 = F.sigmoid(self.lnn2(l1))
        output = self.lnn3(l2)
        return output

    def save(self, fileName="Model.pth"):
        modelFolderPath = "./model/model"
        if not os.path.exists(modelFolderPath):
            os.makedirs(modelFolderPath)

        fileName = os.path.join(modelFolderPath, fileName)
        torch.save(self.state_dict(), fileName)

    def load(self, fileName="Model.pth"):
        modelFolderPath = "./model/model"
        if os.path.exists(modelFolderPath):
            fileName = os.path.join(modelFolderPath, fileName)
            self.load_state_dict(torch.load(fileName))
            self.eval()

class QTrainer:
    def __init__(self, model, learning_rate, gamma, device):
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.learning_rate)
        self.criteria = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype = torch.float).to(self.device)
        action = torch.tensor(action, dtype = torch.long).to(self.device)
        reward = torch.tensor(reward, dtype = torch.float).to(self.device)
        next_state = torch.tensor(next_state, dtype = torch.float).to(self.device)

        if len(state.shape) == 1:
            # This fakes batches so that the NN will work properly
            state = torch.unsqueeze(state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            next_state = torch.unsqueeze(next_state, 0)
            done = (done, )

            prediction = self.model(state)
            target = prediction.clone()

            for i in range(len(done)):
                qNew = reward[i]
                if done[i]:
                    qNew = reward[i] + self.gamma * torch.max(self.model(next_state[i]))

                target[i][action[i]] = qNew

            self.optimizer.zero_grad() # resets gradient for next loss
            loss = self.criteria(target, prediction)
            loss.backward()
            self.optimizer.step()