import tweepy
import operator
from datetime import datetime, timedelta


class RankedTweet:
  def __init__(self, text, retweet_count, favorite_count, created_date, screen_name):
    self.text = text
    self.screen_name = screen_name
    self.created_date = created_date
    self.total_score = favorite_count + (2 * retweet_count)


sources = ['sniptoday', 'WSJ', 'TheEconomist', 'GoogleNews', 'BBCWorld', 'BBCBreaking', 'NPR', 'nprnews', 'USATODAY',
           'PBS', 'Bloomberg', 'CBS', 'NBC', 'aljazeera']


def main(args=None):
  key = 'rbtMI9nYvHFwyF8k16kY8xkc5'
  secret = 'RexJrEz4YOWIS0nKkiu6EVjSyvqbqYpWnhHO3MNJd9pAwn1Kz4'
  auth = tweepy.AppAuthHandler(key, secret)
  api = tweepy.API(auth, wait_on_rate_limit=True)

  total_tweets = []
  for source in sources:
    print('Gathering tweets from ', source)
    res = api.user_timeline(screen_name=source, count=1000)
    total_tweets = total_tweets + gather_ranked_tweets(res)

  total_tweets.sort(key=operator.attrgetter('total_score'))
  i = 0

  print('\n Here is your daily news roundup: \n')
  for tweet in reversed(total_tweets[:1000]):
    i = i + 1
    print(i, ') ', tweet.screen_name, tweet.text, 'total score:', tweet.total_score, 'created:', tweet.created_date)


def gather_ranked_tweets(res):
  ranked_tweets = []
  for status in res:
    # print(dir(status))
    # print(status.text, status.retweet_count, status.favorite_count, status.user.screen_name)
    ranked_tweets.append(RankedTweet(status.text, status.retweet_count, status.favorite_count, status.created_at,
                                     status.user.screen_name))
  ranked_tweets.sort(key=operator.attrgetter('total_score'))

  now = datetime.now()
  trimmed_tweets = []
  for tweet in ranked_tweets:
    # print(tweet.text, tweet.total_score, tweet.created_date)

    if now - timedelta(hours=24) <= tweet.created_date:
      trimmed_tweets.append(tweet)

  return trimmed_tweets


if __name__ == '__main__':
  main(args=None)
