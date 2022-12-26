import numpy as np
import cv2

def get_video_frames(video_path):
    video_read = skvideo.io.vread(video_path)
    video_list = []

    for frame in video_read:
        video_list.append(frame)
    return video_list
