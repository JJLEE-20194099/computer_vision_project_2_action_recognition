import torch

class Loader(torch.utils.data.Dataset):
    def __init__(self, data_path, label_path):
        self.data_path = data_path
        self.label_path = label_path

        self.load_data()
    
    def load_data(self):
        pass