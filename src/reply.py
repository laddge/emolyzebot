import os
import re
import time
import tweepy
from io import BytesIO
from .genimg import genimg

CK = os.getenv("TW_CK")
CS = os.getenv("TW_CS")
AT = os.getenv("TW_AT")
AS = os.getenv("TW_AS")
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)
api = tweepy.API(auth)
limited = False


def reply(status, pid):
    global limited
    if limited:
        time.sleep(900)
    for _ in range(3):
        try:
            parent = api.get_status(pid)
            text = re.sub(
                r"https?://[\w!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+", "", parent.text)
            buff = BytesIO(genimg(text))
            api.update_status_with_media(
                status="@" + status.user.screen_name,
                filename="img.png", file=buff, in_reply_to_status_id=status.id)
        except Exception as e:
            print(e)
            limited = True
            time.sleep(900)
        else:
            break


class Stream(tweepy.Stream):
    def on_status(self, status):
        if status.in_reply_to_status_id:
            reply(status, status.in_reply_to_status_id)
        else:
            if status.text[0:4] == "RT @":
                return
            if not status.quoted_status_id:
                return
            reply(status, status.in_reply_to_status_id)


def main():
    stream = Stream(CK, CS, AT, AS)
    stream.filter(track=["@emolyzebot"], threaded=True)
