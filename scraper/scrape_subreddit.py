# @Author: ramya <ramya>
# @Date:   2017-03-19T21:24:39+01:00
# @Last modified by:   ramya
# @Last modified time: 2017-03-31T15:26:55+02:00

import praw
import time
import os
import pickle
import csv


with open("access/reddit_access.pkl", "rb") as handle:
    access_info = pickle.load(handle)

r = praw.Reddit(client_id = access_info.get("client_id"),
                client_secret = access_info.get("client_secret"),
                password = access_info.get("password"),
                user_agent = "trial with reddit",
                username = access_info.get("username")
        )


subName = "jokes"
folderName=str("reddit_" + subName)
if not os.path.exists(folderName):
    os.makedirs(folderName)



subreddit = r.subreddit(subName)
try:
    with open(folderName + "/timestamp.txt", "r") as k:
        endTime = (float(k.read()))
except:
    startTime = 1104537600.0
    endTime = 1490981608.0

for submission in subreddit.submissions(start = 1104537600.0, end = endTime): # = 1104537600):    ##start time stamp = 1/1/2005
    with open(folderName + "/jokes.txt", "a") as f:
        #writer = csv.writer(f)
        try:
            if submission.score >= 2:
                title = submission.title
                text = submission.selftext
                f.write(title + " " + text.replace("\n", " ") + "\n")
                print(title, submission.selftext, submission.score)
                time.sleep(2)
            else:
                print("excluded 1", submission.score)
                time.sleep(2)
        except:
            print("waiting 5 sec")
            time.sleep(5)
        finally:
            with open(folderName + "/timestamp.txt", "w") as g:
                g.write(str(submission.created))
