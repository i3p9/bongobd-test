from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random
import socket

def is_not_blank(s):
    return bool(s and not s.isspace())


def internetCheck(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as err:
        print(err)
        return False


def loadCompletely():
    # Wait for content to load, then scroll down twice
    # to load all content on home
    time.sleep(4)
    try:
        html = driver.find_element(By.TAG_NAME,'html')
    except:
        print("Website has not loaded yet")
    html.send_keys(Keys.END)
    time.sleep(1)
    html.send_keys(Keys.END)
    time.sleep(6)

def checkForAds():
    print("Checking for advertisements...", end=" ")
    timeChecker1 = driver.find_element(By.XPATH,'//div[contains(@id,"vod_ima-countdown-div")]').text
    time.sleep(3)
    timeChecker2 = driver.find_element(By.XPATH,'//div[contains(@id,"vod_ima-countdown-div")]').text

    if is_not_blank(timeChecker2) == False:
        print("[No ads found]")
        return #Stop checking for ads since it's not present
    else: print("[Found ads]")

    adTime = int(timeChecker2[-2:])
    if timeChecker1 != timeChecker2:
        print("[Advertisement] Is playing...["+adTime+" seconds remaining approx.]")
    time.sleep(adTime+2)
    print("[Advertisement] Is done playing...")

def getVideoPlaybackStatus():
    print("Getting video playback status...")
    time.sleep(10) #Wait 10 seconds for video to play (due to network issue)
    progressTime = driver.find_element(By.XPATH,'//div[contains(@class,"vjs-progress-holder")]').get_attribute("aria-valuenow")
    ButtonStatus = driver.find_element(By.XPATH,'//button[contains(@class, "vjs-play-control")]').get_attribute("title")
    playButton = driver.find_element(By.XPATH,'//button[contains(@class, "vjs-play-control")]')
    #altbuttonStatus = driver.find_element(By.XPATH,'//button[contains(@class, "bongo-big-play-button")]').get_attribute("title")

    # Click the play button if video doesn't play automatically
    if ButtonStatus == "Play":
        playButton.click()
        time.sleep(2)

    # Using both the label of Play/Pause button and the video progress in mm:ss
    # to determine whether or not the video is playing
    # Using one of them might not give the most accurate result

    if (float(progressTime) > 0.00 and ButtonStatus == "Pause"): # Video is playing
        return True
    else: # Not Playing
        internetStatus = internetCheck()
        if internetStatus == True:
            print("Device is connected to internet but can not load the site")
        else:
            print("Device is not connected to the internet")
        return False

def getVideoTitle():
    # Get video title from the <title> tag, stript the "BONGO |" from the title
    vidTitle = driver.title
    if ('|' not in vidTitle):
        time.sleep(3)
        vidTitle = vidTitle.split('| ', 1)[-1]
    elif('|' in vidTitle):
        vidTitle = vidTitle.split('| ', 1)[-1]
    return str(vidTitle)


def getFreeVideos():
    # Find only the free videos via xpath and excluding the ones with Exclusive Span
    freeVids = driver.find_elements(By.XPATH,'//a[contains(@href,"watch") and not(contains(.//span, "Exclusive"))]//div[contains(@class,"MuiCardMedia-root")]/parent::div')

    return freeVids


if __name__ == "__main__":
    print("===Starting up the video playback flow===")
    try:
        s=Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s)
        try:
            driver.get("https://bongobd.com/")
        except:
            print("[Exiting] Can not reach Bongobd website")
            exit()
    except:
        print("[Exiting] Not connected to the internet")
        exit()
    loadCompletely()
    vids = getFreeVideos()

    if len(vids)<1:
        print("[Exiting] No videos found on the webpage")
        exit()

    print("Found "+ str(len(vids)) + " free videos on page via xpath")
    print("Clicking one random free video...")
    vids[random.randint(0,len(vids))].click()
    time.sleep(3)
    checkForAds()
    vidTitle = getVideoTitle()
    vidStatus = getVideoPlaybackStatus()
    if vidStatus == True:
        print("[Result] Video has loaded and currently playing")
        print("[Video Title] ",vidTitle)
    else:
        print("[Result] Video is not playing")
