#the program calcilate the score of pros and cons of a topic,which can be used to create the attitude bar later. The program also shows how many tweets in total has been used.
Import google.cloud 
import tweepy
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

def i=0
def j=0
def K=0
def t=''
client = language.LanguageServiceClient()
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
screen_name = "US Open Tennis Thiem"
count = 5
statuses = api.user_timeline(screen_name, count = count)
for status in statuses:  
      print("Location: " + str(usr.location))
      text =status.text
      document = types.Document(
          content=text,
          type=enums.Document.Type.PLAIN_TEXT)
          sentiment = client.analyze_sentiment(document=document).document_sentiment
          i=i+sentiment.score;
          j=j+1;
          if ((setiment.score>=0.25)&&(setiment.score<=0.75)):
            k=k+1;
            i=i-setiment.score;
          
          
i=i/j          
print('Text: {}'.format(text))
print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))
print('the avarage number is',i,'calculate from',k,'datas','in which',j,'is considered.')
