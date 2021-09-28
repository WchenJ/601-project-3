Import google.cloud 
import tweepy
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

client = language.LanguageServiceClient()
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
screen_name = "US Open Tennis"
count = 3
statuses = api.user_timeline(screen_name, count = count)
for status in statuses:  
      text =status.text
      document = types.Document(
          content=text,
          type=enums.Document.Type.PLAIN_TEXT)
          sentiment = client.analyze_sentiment(document=document).document_sentiment

print('Text: {}'.format(text))
print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))