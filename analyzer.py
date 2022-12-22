import torch
import numpy as np
from transformers import BertTokenizer

import sys
sys.path.append('utils')
from clf import *

class Analyzer():
    def __init__(self, weights_path):
        self.device = torch.device('cpu' if not torch.cuda.is_available() else 'cuda:0')
        self.model = BertCLF(hidden_neurons=512)
        self.model.load_state_dict(torch.load(weights_path, map_location=self.device))
        self.model.to(self.device).eval()
        self.tokenizer = BertTokenizer.from_pretrained('DeepPavlov/rubert-base-cased')

    def predict_label(self, text):
        input_ids, attention_mask = self.preprocess_text(text)
        input_ids, attention_mask = input_ids.to(self.device), attention_mask.to(self.device)
        with torch.no_grad():
            pred_prob = self.model.forward(input_ids, attention_mask)
        pred_prob = torch.nn.Sigmoid()(pred_prob).squeeze(0)
        pred_prob = pred_prob.detach().to('cpu').numpy()
        pred_label = np.where(pred_prob > 0.5, 1, 0)
        pred_label = 'Human' if pred_label == 0 else 'Machine'
        return pred_label, round(pred_prob.item(), 2)

    def preprocess_text(self, text):
        tokens = self.tokenizer.tokenize('[CLS] ' + text[:512] + ' [SEP]')
        input_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        attention_mask = [float(i>0) for i in input_ids]

        input_ids = torch.tensor(input_ids)
        attention_mask = torch.tensor(attention_mask)
        return input_ids.unsqueeze(0), attention_mask.unsqueeze(0)