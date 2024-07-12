import praw
import pymongo
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import src.cleaning as cleaning
import src.tickers as tickers
from dotenv import load_dotenv
import os
from collections import defaultdict
import numpy as np

# Load env variables from .env
load_dotenv()

# List of subreddits to use
subreddits = ["Investing", "StockMarket", "Stocks", "Trading"]

# Create a reddit client
reddit = praw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    user_agent=os.getenv('USER_AGENT')
)

# Set up MongoDB connection
client = pymongo.MongoClient(os.getenv('MONGODB_URI'))
db = client.reddit_data
collection = db.posts

# Initialize analyzer
obj = SentimentIntensityAnalyzer()

# Set up default dictionary
sentiment_dict = defaultdict(list)

found_tickers = []

for subreddit in subreddits:
    # Fetch submissions for each subreddit
    for submission in reddit.subreddit(subreddit).hot(limit=10):
        cleaned = cleaning.remove_usernames(cleaning.remove_urls(submission.selftext))
        submission_tickers = tickers.find_tickers(cleaned)  # Stores tickers found in each cleaned submission
        found_tickers.extend(tickers.find_tickers(cleaned))

        # Calculate sentiment scores (including compound, pos, neu, neg) of the cleaned data
        sentiment_scores = obj.polarity_scores(cleaned)

        # Use compound score to determine whether the content is positive, negative, or neutral
        sentiment = 'positive' if sentiment_scores['compound'] >= 0.1 else 'negative' if sentiment_scores['compound'] <= -0.1 else 'neutral'

        # Append the sentiment scores for each ticker found in the submission
        for ticker in submission_tickers:
            sentiment_dict[ticker].append(sentiment_scores)

        # Store the data of the posts
        post_data = {
            'title': submission.title,
            'content': cleaned,
            'timestamp': submission.created_utc,
            'subreddit': subreddit,
            'ticker': found_tickers
        }
        collection.insert_one(post_data)

print("TICKERS FOUND: ", found_tickers)

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

print("TICKERS FOUND: ", found_tickers)
print("AVERAGE SENTIMENTS OF EACH TICKER: ", average_sentiment_scores)
