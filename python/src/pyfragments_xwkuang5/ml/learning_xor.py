import torch
import torch.nn as nn
import torch.nn.functional as F

from torch.utils.data import DataLoader
from torch.utils.data.dataset import Dataset


class XORModel(nn.Module):

    def __init__(self):
        super(XORModel, self).__init__()

        num_hidden = 4

        self.hidden = nn.Linear(2, num_hidden)
        self.output = nn.Linear(num_hidden, 2)

    def forward(self, x):

        x = self.hidden(x) 
        x = F.relu(x)
        x = self.output(x)
        return F.log_softmax(x)


class XORData(Dataset):

    def __init__(self):
        super(XORData, self).__init__()
        self._inputs = torch.tensor([
            [0, 0],
            [0, 1],
            [1, 0],
            [1, 1]
        ], dtype=torch.float32)

        self._targets = torch.tensor([
            0, 1, 1, 0
        ])

    def __getitem__(self, index):

        return (self._inputs[index], self._targets[index])
    
    def __len__(self):

        return len(self._inputs)

model = XORModel()
optimizer = torch.optim.SGD(model.parameters(), lr=1e-1)
loss_function = torch.nn.NLLLoss()

data = XORData()
data_loader = DataLoader(data, batch_size=4, shuffle=True)

epochs = 1000

model.train()
for epoch in range(0, epochs):

    for idx, (inputs, targets) in enumerate(data_loader):
        optimizer.zero_grad()

        outputs = model(inputs)
        loss = loss_function(outputs, targets)
        loss.backward()
        optimizer.step()

    if epoch % 100 == 0:
        print('Loss: {:.2f}'.format(loss.item()))

model.eval()
with torch.no_grad():
    n = len(data)
    test_loader = DataLoader(data, batch_size=n, shuffle=False)
    inputs_, targets = next(iter(test_loader))

    outputs = model(inputs_)
    _, predictions = torch.max(outputs, dim=1, keepdim=False)

    num_correct = torch.sum(predictions.eq(targets.view_as(predictions)))
    print('Accuracy: {}'.format(num_correct / n))