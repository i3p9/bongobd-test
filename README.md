# Bongobd-test

Repo for Bongo SQA Code Test

## Running

Install pip package requirements
```bash
pip3 install -r requirements.txt
```
And finally run the test by running `main.py`

> Note: There are some usage of `time.sleep()` because the network that the script was tested on was slow and thus took time to load content compared to when browsing the website with a good internet connection.
> sleep timer can be lowered dramatically when testing on a better network

## Result

When a video without an advertisement is successfully played

```bash
===Starting up the video playback flow===
[WDM] -
[WDM] - ====== WebDriver manager ======
[WDM] - Current google-chrome version is 95.0.4638
Found 36 free videos on page via xpath
Clicking one random free video...
Checking for advertisements... [No ads found]
Getting video playback status...
[Result] Video has loaded and currently playing
[Video Title] Katmundu
```

and when a video with an advertisement is successfully played

```bash
===Starting up the video playback flow===
[WDM] -
[WDM] - ====== WebDriver manager ======
[WDM] - Current google-chrome version is 95.0.4638
Found 36 free videos on page via xpath
Clicking one random free video...
Checking for advertisements... [Found ads]
[Advertisement] Is playing...[04 seconds remaining approx.]
[Advertisement] Is done playing...
Getting video playback status...
[Result] Video has loaded and currently playing
[Video Title] Katmundu
```
