import torch
from torch.nn import functional as F
from transformers import BertConfig, BertModel


class BertCLF(torch.nn.Module):
    def __init__(self, hidden_neurons):
        super(BertCLF, self).__init__()
        config = BertConfig.from_pretrained('DeepPavlov/rubert-base-cased', num_labels=2)
        self.model = BertModel.from_pretrained('DeepPavlov/rubert-base-cased', config=config)
        self.hidden_neurons = hidden_neurons
        self.linear1 = torch.nn.Linear(config.hidden_size, self.hidden_neurons)
        self.linear2 = torch.nn.Linear(self.hidden_neurons, int(self.hidden_neurons / 2))
        self.classifier = torch.nn.Linear(int(self.hidden_neurons / 2), 1)
        self.dropout = torch.nn.Dropout(.3)
        self.batchnorm1 = torch.nn.BatchNorm1d(self.hidden_neurons)
        self.batchnorm2 = torch.nn.BatchNorm1d(int(self.hidden_neurons / 2))

    def forward(self, input_ids, attention_mask):
        bert_output = self.model(input_ids=input_ids, attention_mask=attention_mask)
        seq_output = bert_output[0]
        pooled_output = seq_output.mean(axis=1)
        pooled_output = self.dropout(pooled_output)
        
        x1 = self.dropout(F.relu(self.batchnorm1(self.linear1(pooled_output))))
        x1 = self.dropout(F.relu(self.batchnorm2(self.linear2(x1))))
        
        scores = self.dropout(self.classifier(x1))
        return scores