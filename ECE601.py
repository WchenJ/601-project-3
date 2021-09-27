# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 22:26:42 2021

@author: bobga
"""


import tweepy
consumer_key="2fMQhM0ylF7LEXCb2VtqRWPyO"
consumer_secret="qOR7SiSpf42W03qv2sWCRqJCV34p7EBQRJtIBOWjyJXyHpS9bf"
access_token="1440896937952174081-hYExZbXZ8OyGjzDnckprzQcHjzxW3Y"
access_token_secret="zcqLHUsRA4Kap4GxZ93pB0VbgHBaFmrityX2hf9NUbsFE"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
screen_name = "US Open Tennis"
count = 3
statuses = api.user_timeline(screen_name, count = count)
for status in statuses:  
  print(status.text, end = "\n\n")