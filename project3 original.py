
from datetime import datetime
startTime = datetime.now()
import json
import tweepy #https://github.com/tweepy/tweepy
import os
from google.cloud import language_v1



def anatweet (str):

      os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/ece/ec601/creds.json"
      client = language_v1.LanguageServiceClient()
      consumer_key = ""
      consumer_secret = ""
      access_key = ""
      access_secret = ""
      auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
      auth.set_access_token(access_key, access_secret)
      api = tweepy.API(auth)

      usr = api.get_user(str)
      stat = api.user_timeline(str, count=10)
      
      for i in stat:
        #print(i.text, end = "\n\n")
        text = i.text
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
        print("Text: {}".format(i.text))
        print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))
        if(sentiment.score < 0 or sentiment.magnitude < 0):
            print('Negative attitude')
        elif(sentiment.score == 0 or sentiment.magnitude == 0):
            print('Neutral attitude')
        elif(sentiment.score > 0 or sentiment.magnitude > 0):
            print('Positive attitude')
      print()
      print('run time:','{}'.format(datetime.now() - startTime))
     

if __name__ == "__main__":
    try:
        anatweet("@US Open Thiem")
    except tweepy.error.TweepError as e:
        print("A mistake occur, please search according to"+ str(e))
