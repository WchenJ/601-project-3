#the program calcilate the score of pros and cons of a topic,which can be used to create the attitude bar later. The program also shows how many tweets in total has been used.
Import google.cloud 
import tweepy
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

i=0
j=0
K=0
t=''
def anatweet(str)

      i=0
      j=0
      K=0
      t=''
      consumer_key = "******"
      consumer_secret = "******"
      access_key = "******"
      access_secret = "******"
      client = language.LanguageServiceClient()
      auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
      auth.set_access_token(access_token, access_token_secret)
      api = tweepy.API(auth)

      specific_user=str
      count = 5

      # print me
      me = api.me()
      print("my id: ",me.id_str, "\nmy screen name: ",me.screen_name)

      # get user
      user = api.get_user(specific_user)
      print("\nUser id: ",user.id_str,"\nScreen Name: ",user.screen_name)

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
      tweets_find = api.search(str,count='20')
      for search_tweet in tweets_find:
          print('\n')
          print('tweet text:',search_tweet.text)
          hashtags=[]
          for tag_inf in search_tweet.entities['hashtags']:
              hashtags.append(tag_inf['text'])
          if len(hashtags)!=0:
              print('tweet hashtag:',hashtags)
      print('\n')
      print('Text: {}'.format(text))
      print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))
      print('the avarage number is',i,'calculate from',k,'datas','in which',j,'is considered.')

if __name__ == "__main__":
    try:
        anatweet("US Open Thiem")
    except tweepy.error.TweepError as e:
        print("A mistake occur, please search according to"+ str(e))



