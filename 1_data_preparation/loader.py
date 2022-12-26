import torch
import os

class Loader(torch.utils.data.Dataset):
    def __init__(self, 
                data_path, 
                label_path,
                num_person_in=5,
                num_person_out=2
                ):
        self.data_path = data_path
        self.label_path = label_path
        self.num_person_in = num_person_in
        self.num_person_out = num_person_out
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
        self.M = self.num_person_out
    
    def __len__(self):
        return len(self.sample_name)
    
    def __iter__(self):
        return self

    def __getitem__(self, index):
        sample_name = self.sample_name[index]
        sampel_path = os.path.join(self.data_path, sample_name)
        with open(sample_path, 'r') as f:
            video_info = json.load(f)
        
        data_numpy = np.zeros((self.C, self.T, self.V, self.num_person_in))

        for frame_info in video_info['data']:
            frame_index = frame_info['frame_index']
            for m, skeleton_info in enumerate(frame_info["skeleton"]):
                if (m >= self.num_person_in):
                    break
                pose = skeleton_info["pose"]
                score = skeleton_info["score"]
                data_numpy[0, frame_index, :, m] = pose[0::2]
                data_numpy[1, frame_index, :, m] = pose[1::2]
                data_numpy[2, frame_index, :, m] = score

        data_numpy[0:2] = data_numpy[0:2] - 0.5
        data_numpy[0][data_numpy[2] == 0] = 0
        data_numpy[1][data_numpy[2] == 0] = 0

        label = video_info["label"]
        assert (label == self.label[index])

        return data_numpy, label


