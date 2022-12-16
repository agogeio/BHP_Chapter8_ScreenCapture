import cv2
import os
from PIL import Image
import pyautogui
import socket 

from datetime import datetime
from time import sleep

#? Will work for other OSs besides Windows without additional 
#? packages being installed, but Windows will work stand alone

#* pip install pyautogui
#* https://pyautogui.readthedocs.io/en/latest/
#* PyAutoGUI only runs on Windows, macOS, and Linux.
#* right now PyAutoGUI only handles the primary monitor
#* On Linux, you must run sudo apt-get install scrot to use the screenshot features.

#* pip install opencv-python
#* https://pypi.org/project/opencv-python/
#* https://docs.opencv.org/4.x/

HOSTNAME = socket.gethostname()
IMAGE_DIR = './images/'
VIDEO_DIR = './videos/'
SLEEP_TIME = .25
FPS = 4
MOVIE_DURATION_IN_FRAMES = 20
IMG_EXT = 'jpg'
VIDEO_EXT = 'mp4'

# def cleanFiles(frames):
#     for frame in frames:
#         # print(frame)
#         # os.remove(frame)
#         pass

def makeMovie(frames, width, height):

    src_width, src_height = pyautogui.size()
    width = int(src_width)
    height = int(src_height)

    now = datetime.now()
    current_time = now.strftime('%H:%M:%S')
    video_filename = f'{HOSTNAME}-{current_time}.{VIDEO_EXT}'
    video_path = f'{VIDEO_DIR}{video_filename}'

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    video = cv2.VideoWriter(video_path, fourcc, FPS, (int(width), int(height)))
    #? VideoWriter takes: output_name, fourcc, fps, size
    #* https://docs.opencv.org/3.4/dd/d9e/classcv_1_1VideoWriter.html

    for frame in frames:
        video.write(cv2.imread(frame))

    video.release()


def getScreen():

    imgs = []
    frame = 0
    cont = True

    src_width, src_height = pyautogui.size()
    width = int(src_width)
    height = int(src_height)
    #? These must be cast to int, will return a float by default

    while cont == True:

        try:
            image_path = f'{IMAGE_DIR}{HOSTNAME}-{frame}.{IMG_EXT}'
            screenshot = pyautogui.screenshot()
            screenshot = screenshot.resize((width, height))
            screenshot.save(image_path)
            imgs.append(image_path)
            frame += 1
            sleep(SLEEP_TIME)
        except Exception as e:
            print(f'Exception: {e}')

        if frame > MOVIE_DURATION_IN_FRAMES:
            # call makeMovie to make the movie
            makeMovie(imgs, width, height)
            frame = 0
            cont = False
            # cleanFiles(imgs)
            # delete the old image frames


getScreen()