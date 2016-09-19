#!/usr/bin/python

import bs4
import gtk
import json
import posix
import re
import subprocess
import sys
import urllib3

def whine(msg, err):
    """Spawn a GTK dialog w/error message."""
    parent = None
    md = gtk.MessageDialog(parent, 
         gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
         gtk.BUTTONS_CLOSE, msg)
    md.run()
    md.destroy()
    sys.exit(err)

def getvideopage(http, watchurl):
    """Extract the embedded video page URL."""
    watchlive = http.request("GET", watchurl)
    if watchlive.status != 200:
        whine("Could not download the Cross Point Watch Live page!",
              posix.EX_UNAVAILABLE)
    soup = bs4.BeautifulSoup(watchlive.data, "lxml")
    videourl=soup.find("iframe", {"id": "playerIFrame"})["src"]
    if videourl == None:
        whine("There is not a live stream posted right now.",
              posix.EX_NOINPUT)
    return videourl

def getkeys(http, videourl):
    """Extract the secret key and event id."""
    video = http.request("GET", videourl)
    if video.status != 200:
        whine("Could not download the embedded video page!",
              posix.EX_UNAVAILABLE)
    soup = bs4.BeautifulSoup(video.data)
    api, uuid = None, None
    for script in soup.find_all("script"):
        for line in script:
            blob = re.sub(r"\s+", "", line)
            if "varflashvars" in blob:
                api = re.search(r'.*clientAPI:"([a-z0-9\-]+)".*', blob)
                uuid = re.search(r'.*eventUUID:"(\w+)".*', blob)
    if api == None or uuid == None:
        whine("Could not extract the API key or UUID number!",
              posix.EX_DATAERR)
    return api, uuid

def getstream(http, api, uuid):
    """Make a request for the current live event."""
    # See https://ovp.piksel.com/services/docs
    # /functions_overview.php?page=rest&apiv=
    streamurl = "http://player.piksel.com/ws/ws_live_event/api/"
    streamurl += api.group(1)
    streamurl += "/mode/json/apiv/5/?uuid="
    streamurl += uuid.group(1)
    stream = http.request("GET", streamurl)
    if stream.status != 200:
        whine("Could not get streaming information!",
              posix.EX_UNAVAILABLE)
    myjson = json.loads(stream.data)
    events = myjson["response"]["WsLiveEventResponse"]["liveEvents"]
    if events == []:
        whine("There is not a live stream posted right now.",
              posix.EX_NOINPUT)
    m3u8 = events[0]["streamPackages"][0]["m3u8"]
    return m3u8

if __name__ == "__main__":
    # Cross Point's Watch Live page
    watchurl = "http://www.crosspoint.tv/internet/watch-live"

    # share our requests
    http = urllib3.PoolManager()

    # turtles all the way down
    videourl = getvideopage(http, watchurl)
    api, uuid = getkeys(http, videourl)
    m3u8 = getstream(http, api, uuid)

    # and finally play the dang thing
    subprocess.Popen(["/usr/bin/mpv", m3u8])
