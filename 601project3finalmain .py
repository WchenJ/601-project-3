#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 16:50:22 2021

@author: ece
"""



import tweepy
import re

import json
from google.cloud import language_v1

from nltk.tokenize import WordPunctTokenizer
from datetime import datetime, timedelta

import os


states = {
            'AL': 'Alabama',
            'AK': 'Alaska',
            'AZ': 'Arizona',
            'AR': 'Arkansas',
            'CA': 'California',
            'CO': 'Colorado',
            'CT': 'Connecticut',
            'DE': 'Delaware',
            'DC': 'District of Columbia',
            'FL': 'Florida',
            'GA': 'Georgia',
            'HI': 'Hawaii',
            'ID': 'Idaho',
            'IL': 'Illinois',
            'IN': 'Indiana',
            'IA': 'Iowa',
            'KS': 'Kansas',
            'KY': 'Kentucky',
            'LA': 'Louisiana',
            'ME': 'Maine',
            'MD': 'Maryland',
            'MA': 'Massachusetts',
            'MI': 'Michigan',
            'MN': 'Minnesota',
            'MS': 'Mississippi',
            'MO': 'Missouri',
            'MT': 'Montana',
            'NE': 'Nebraska',
            'NV': 'Nevada',
            'NH': 'New Hampshire',
            'NJ': 'New Jersey',
            'NM': 'New Mexico',
            'NY': 'New York',
            'NC': 'North Carolina',
            'ND': 'North Dakota',
            'OH': 'Ohio',
            'OK': 'Oklahoma',
            'OR': 'Oregon',
            'PA': 'Pennsylvania',
            'RI': 'Rhode Island',
            'SC': 'South Carolina',
            'SD': 'South Dakota',
            'TN': 'Tennessee',
            'TX': 'Texas',
            'UT': 'Utah',
            'VT': 'Vermont',
            'VA': 'Virginia',
            'WA': 'Washington',
            'WV': 'West Virginia',
            'WI': 'Wisconsin',
            'WY': 'Wyoming'
         }
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="  "
CONS_KEY = " "
CONS_SECRET = " "
ACC_TOKEN = " "
ACC_SECRET = " "


def authentication(cons_key, cons_secret, acc_token, acc_secret):
    auth = tweepy.OAuthHandler(cons_key, cons_secret)
    auth.set_access_token(acc_token, acc_secret)
    api = tweepy.API(auth)
    return api


def search_tweets(keyword, total_tweets):
    today_datetime = datetime.today().now()
    yesterday_datetime = today_datetime - timedelta(days=7)
    today_date = today_datetime.strftime('%Y-%m-%d')
    yesterday_date = yesterday_datetime.strftime('%Y-%m-%d')
    api = authentication(CONS_KEY,CONS_SECRET,ACC_TOKEN,ACC_SECRET)
    search_result = tweepy.Cursor(api.search_tweets, 
                                  q=keyword, 
                                  since=yesterday_date, 
                                  result_type='recent', 
                                  lang='en').items(total_tweets)  
    return search_result


def clean_tweets(tweet):
    user_removed = re.sub(r'@[A-Za-z0-9]+','',tweet.decode('utf-8'))
    link_removed = re.sub('https?://[A-Za-z0-9./]+','',user_removed)
    number_removed = re.sub('[^a-zA-Z]', ' ', link_removed)
    lower_case_tweet= number_removed.lower()
    tok = WordPunctTokenizer()
    words = tok.tokenize(lower_case_tweet)
    clean_tweet = (' '.join(words)).strip()
    return clean_tweet

    
def get_sentiment_score(tweet):
        i=0
        j=0
        k=0
        t=''
        client = language_v1.LanguageServiceClient()
        text = tweet.text
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
        i=i+sentiment.score
                   
        return sentiment.score,sentiment.magnitude


def extract_place(status):
    if type(status) is tweepy.models.Status:
        status = status.__dict__
    #Try to get the place from the place data inside the status dict
    if status['place'] is not None:
        place = status['place']
        if place['country'] != 'United States':
            return place['country']
        elif place['place_type'] == 'admin':
            return place['name']
        elif place['place_type'] == 'city':
            return states.get(place['full_name'].split(', ')[-1])
    #If the status dict has no place info, get the place from the user data
    else:
        place = status['user']['location']
        try:
            place = place.split(', ')[-1].upper()
        except AttributeError:
            return None
        if place in states:
            return states[place]
        else:
            return place


def recognize(keyword):
    if keyword[0]=='@':
        return 1
    else:
        return 0
def analyze_tweets(keyword, total_tweets):
    try:
            p=recognize(keyword)
            if p==0:
                    total = 0
                    j=0
                    k=0
                    g=0
                    t1=''
                    t2=''
                    t=''
                    tt=''
                    tweets = search_tweets(keyword,total_tweets)
                    for tweet in tweets:
                         cleaned_tweet = clean_tweets(tweet.text.encode('utf-8'))
                         score, magnitude = get_sentiment_score(tweet)
                         total+= int(magnitude)*int(score)
                         j=j+1
                         if ((score>=0.2)|(score<=-0.2)|(score==0)):
                                    if score==0:
                                                g=g+1
                                    if score>0:
                                                t1=t1+'*'
                                    if score<0:
                                                t2=t2+'|'
                                    k=k+1
                         else:
                                    total=total-magnitude*score 
                     t=t+'     ['+t1+t2+']     '
                     tt='positive'+(len(t1)+len(t2)-4)*' '+'negative'
                     print('\n')
                     print("the total score is %s \n"%(total))
                     print('here is the attitude contradiction bar \n \n')
                     print(t)
                     print(tt)
                     print('\n \n')
                     if k==0:
                        print('no sample is considered useful for calculating the attitude')
                     if (total>0)&(k!=0):
                        print("the attitude is POSITIVE \n which is calculate from %s samples in which %s samples has been count and %s is neutral"%(j,k,g))
                     if (total<0)&(k!=0):
                        print("the attitude is NEGATIVE \n which is calculate from %s samples in which %s samples has been count and %s is neutral"%(j,k,g))
                     if (total==0)&(k!=0):
                        print("the attitude is NEUTRAL \n which is calculate from %s samples in which %s samples has been count"%(j,k))
                     if (total_tweets>=80):
                        print("Twitter API only afford to count in 80 tweets, the tweets out of 80 are no included.")
                     return total
             else:
                     api = authentication(CONS_KEY,CONS_SECRET,ACC_TOKEN,ACC_SECRET)
                     usr = api.get_user(screen_name=keyword)
                     print("Location: " + str(usr.location))
                     return 0
    except tweepy.TweepyException as e:
             print("A mistake occur, please search according to: \n"+ str(e))
             return 0
def main():
        analyze_tweets('US open Thiem',50)
        analyze_tweets('@ThiemDomi',50)
        analyze_tweets('@1',50)
    

    
if __name__ == '__main__#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 16:50:22 2021

@author: ece
"""



import tweepy
import re

import json
from google.cloud import language_v1

from nltk.tokenize import WordPunctTokenizer
from datetime import datetime, timedelta

import os


states = {
            'AL': 'Alabama',
            'AK': 'Alaska',
            'AZ': 'Arizona',
            'AR': 'Arkansas',
            'CA': 'California',
            'CO': 'Colorado',
            'CT': 'Connecticut',
            'DE': 'Delaware',
            'DC': 'District of Columbia',
            'FL': 'Florida',
            'GA': 'Georgia',
            'HI': 'Hawaii',
            'ID': 'Idaho',
            'IL': 'Illinois',
            'IN': 'Indiana',
            'IA': 'Iowa',
            'KS': 'Kansas',
            'KY': 'Kentucky',
            'LA': 'Louisiana',
            'ME': 'Maine',
            'MD': 'Maryland',
            'MA': 'Massachusetts',
            'MI': 'Michigan',
            'MN': 'Minnesota',
            'MS': 'Mississippi',
            'MO': 'Missouri',
            'MT': 'Montana',
            'NE': 'Nebraska',
            'NV': 'Nevada',
            'NH': 'New Hampshire',
            'NJ': 'New Jersey',
            'NM': 'New Mexico',
            'NY': 'New York',
            'NC': 'North Carolina',
            'ND': 'North Dakota',
            'OH': 'Ohio',
            'OK': 'Oklahoma',
            'OR': 'Oregon',
            'PA': 'Pennsylvania',
            'RI': 'Rhode Island',
            'SC': 'South Carolina',
            'SD': 'South Dakota',
            'TN': 'Tennessee',
            'TX': 'Texas',
            'UT': 'Utah',
            'VT': 'Vermont',
            'VA': 'Virginia',
            'WA': 'Washington',
            'WV': 'West Virginia',
            'WI': 'Wisconsin',
            'WY': 'Wyoming'
         }
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="  "
CONS_KEY = " "
CONS_SECRET = " "
ACC_TOKEN = " "
ACC_SECRET = " "


def authentication(cons_key, cons_secret, acc_token, acc_secret):
    auth = tweepy.OAuthHandler(cons_key, cons_secret)
    auth.set_access_token(acc_token, acc_secret)
    api = tweepy.API(auth)
    return api


def search_tweets(keyword, total_tweets):
    today_datetime = datetime.today().now()
    yesterday_datetime = today_datetime - timedelta(days=7)
    today_date = today_datetime.strftime('%Y-%m-%d')
    yesterday_date = yesterday_datetime.strftime('%Y-%m-%d')
    api = authentication(CONS_KEY,CONS_SECRET,ACC_TOKEN,ACC_SECRET)
    search_result = tweepy.Cursor(api.search_tweets, 
                                  q=keyword, 
                                  since=yesterday_date, 
                                  result_type='recent', 
                                  lang='en').items(total_tweets)  
    return search_result


def clean_tweets(tweet):
    user_removed = re.sub(r'@[A-Za-z0-9]+','',tweet.decode('utf-8'))
    link_removed = re.sub('https?://[A-Za-z0-9./]+','',user_removed)
    number_removed = re.sub('[^a-zA-Z]', ' ', link_removed)
    lower_case_tweet= number_removed.lower()
    tok = WordPunctTokenizer()
    words = tok.tokenize(lower_case_tweet)
    clean_tweet = (' '.join(words)).strip()
    return clean_tweet

    
def get_sentiment_score(tweet):
        i=0
        j=0
        k=0
        t=''
        client = language_v1.LanguageServiceClient()
        text = tweet.text
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
        i=i+sentiment.score
                   
        return sentiment.score,sentiment.magnitude


def extract_place(status):
    if type(status) is tweepy.models.Status:
        status = status.__dict__
    #Try to get the place from the place data inside the status dict
    if status['place'] is not None:
        place = status['place']
        if place['country'] != 'United States':
            return place['country']
        elif place['place_type'] == 'admin':
            return place['name']
        elif place['place_type'] == 'city':
            return states.get(place['full_name'].split(', ')[-1])
    #If the status dict has no place info, get the place from the user data
    else:
        place = status['user']['location']
        try:
            place = place.split(', ')[-1].upper()
        except AttributeError:
            return None
        if place in states:
            return states[place]
        else:
            return place


def recognize(keyword):
    if keyword[0]=='@':
        return 1
    else:
        return 0
def analyze_tweets(keyword, total_tweets):
    try:
            p=recognize(keyword)
            if p==0:
                    total = 0
                    j=0
                    k=0
                    g=0
                    t1=''
                    t2=''
                    t=''
                    tt=''
                    tweets = search_tweets(keyword,total_tweets)
                    for tweet in tweets:
                         cleaned_tweet = clean_tweets(tweet.text.encode('utf-8'))
                         score, magnitude = get_sentiment_score(tweet)
                         total+= int(magnitude)*int(score)
                         j=j+1
                         if ((score>=0.2)|(score<=-0.2)|(score==0)):
                                    if score==0:
                                                g=g+1
                                    if score>0:
                                                t1=t1+'*'
                                    if score<0:
                                                t2=t2+'|'
                                    k=k+1
                         else:
                                    total=total-magnitude*score 
                     t=t+'     ['+t1+t2+']     '
                     tt='positive'+(len(t1)+len(t2)-4)*' '+'negative'
                     print('\n')
                     print("the total score is %s \n"%(total))
                     print('here is the attitude contradiction bar \n \n')
                     print(t)
                     print(tt)
                     print('\n \n')
                     if k==0:
                        print('no sample is considered useful for calculating the attitude')
                     if (total>0)&(k!=0):
                        print("the attitude is POSITIVE \n which is calculate from %s samples in which %s samples has been count and %s is neutral"%(j,k,g))
                     if (total<0)&(k!=0):
                        print("the attitude is NEGATIVE \n which is calculate from %s samples in which %s samples has been count and %s is neutral"%(j,k,g))
                     if (total==0)&(k!=0):
                        print("the attitude is NEUTRAL \n which is calculate from %s samples in which %s samples has been count"%(j,k))
                     if (total_tweets>=80):
                        print("Twitter API only afford to count in 80 tweets, the tweets out of 80 are no included.")
                     return total
            else:
                     api = authentication(CONS_KEY,CONS_SECRET,ACC_TOKEN,ACC_SECRET)
                     usr = api.get_user(screen_name=keyword)
                     print("Location: " + str(usr.location))
                     return 0
    except tweepy.TweepyException as e:
             print("A mistake occur, please search according to: \n"+ str(e))
             return 0
def main():
        analyze_tweets('US open Thiem',50)
        analyze_tweets('@ThiemDomi',50)
        analyze_tweets('@1',50)
    

    
if __name__ == '__main__':
    main()
