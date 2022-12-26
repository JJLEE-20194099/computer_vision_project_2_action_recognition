import torch
import os

class Loader(torch.utils.data.Dataset):
    def __init__(self, 
                data_path, 
                label_path,
                num_person=2
                ):
        self.data_path = data_path
        self.label_path = label_path
        self.num_person = num_person
        self.load_data()
    
    def load_data(self):
        
        label_path = self.label_path
        with open(label_path) as f:
            label_info = json.load(f)
        
        self.sample_name = os.listdir(self.data_path)

        sample_id_list = [name.split('.')[0] for name in self.sample_name]
        self.label = np.array(label_info[id]['label_index'] for id in sample_id_list)
        
        has_skeleton_list = np.array([label_info[id]['has_skeleton'] for id in sample_id_list])

        self.sample_name = [s for has_skeleton, s in zip(has_skeleton_list, sample_id_list) if has_skeleton]
        self.label = self.label[has_skeleton_list]

        # Kích thước data
        self.N = len(self.sample_name)  
        # Số channels
        self.C = 3
        # Khoảng frame
        self.T = 300
        # Lấy 18 keypoints đối với 1 person
        self.V = 18
        # Lấy bao nhiêu person
        self.M = self.num_person