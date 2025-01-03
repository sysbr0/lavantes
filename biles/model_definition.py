import torch.nn as nn
import torch.optim as optim

# Define a simple neural network
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(3, 64)  # 3 input features (price, net, top)
        self.fc2 = nn.Linear(64, 32)  # 64 neurons in the hidden layer
        self.fc3 = nn.Linear(32, 1)  # 1 output (whether done or not)
        self.sigmoid = nn.Sigmoid()  # Sigmoid activation for binary classification
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.sigmoid(self.fc3(x))  # Output between 0 and 1
        return x

# Initialize the model
model = SimpleNN()

# Loss and optimizer
criterion = nn.BCELoss()  # Binary Cross-Entropy loss
optimizer = optim.Adam(model.parameters(), lr=0.001)
