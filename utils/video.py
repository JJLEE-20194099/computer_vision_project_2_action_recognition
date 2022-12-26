import numpy as np
import cv2

def get_video_frames(video_path):
    video_read = skvideo.io.vread(video_path)
    video_list = []

    for frame in video_read:
        video_list.append(frame)
    return video_list

def play_video(video_path, fps=30):
    cap = cv2.VideoCapture(video_path)

    while(cap.isOpened()):
        _, frame = cap.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', gray_frame)

        if (cv2.waitKey(1000/fps) & 0xFF == ord('q')):
            break
    
    cap.release()
    cv2.destroyAllWindows()
