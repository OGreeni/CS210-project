# TODO: given a string of text, analyze the sentiment (i.e., positive or negative)
import praw
import pymongo
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import cleaning
import tickers
from dotenv import load_dotenv
import os
from collections import defaultdict
import numpy as np
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import db, subreddits, reddit

# Initialize analyzer
obj = SentimentIntensityAnalyzer()

# Set up default dictionary
sentiment_dict = defaultdict(list)

for subreddit in subreddits:
    # Fetch submissions for each subreddit
    for submission in reddit.subreddit(subreddit).hot(limit=10):
        cleaned = cleaning.remove_usernames(cleaning.remove_urls(submission.selftext))
        submission_tickers = tickers.find_tickers(cleaned)  # Stores tickers found in each cleaned submission

        # Calculate sentiment scores (including compound, pos, neu, neg) of the cleaned data
        sentiment_scores = obj.polarity_scores(cleaned)

        # Use compound score to determine whether the content is positive, negative, or neutral
        sentiment = 'positive' if sentiment_scores['compound'] >= 0.1 else 'negative' if sentiment_scores[
                                                                                             'compound'] <= -0.1 else 'neutral'

        # Append the sentiment scores for each ticker found in the submission
        for ticker in submission_tickers:
            sentiment_dict[ticker].append(sentiment_scores)

average_sentiment_scores = {}

# Averages sentiment scores across all submissions for each ticker
for ticker, sentiments in sentiment_dict.items():
    average_sentiment = {
        'compound': np.mean([s['compound'] for s in sentiments]),
        'pos': np.mean([s['pos'] for s in sentiments]),
        'neu': np.mean([s['neu'] for s in sentiments]),
        'neg': np.mean([s['neg'] for s in sentiments]),
    }
    average_sentiment_scores[ticker] = average_sentiment

average_sentiment_collection = db.average_sentiments

# Store the averages in a MongoDB collection
for ticker, average_sentiment in average_sentiment_scores.items():
    average_sentiment_collection.insert_one({
        'ticker': ticker,
        'average_sentiment': average_sentiment
    })

print("AVERAGE SENTIMENTS OF EACH TICKER: ", average_sentiment_scores)
