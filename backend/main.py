import praw
import pymongo
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import src.cleaning as cleaning
import src.tickers as tickers
from dotenv import load_dotenv
import os
from collections import defaultdict
import numpy as np
import requests
import datetime
import matplotlib.pyplot as plt

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

print("AVERAGE SENTIMENTS OF EACH TICKER: ", average_sentiment_scores)

# Retrieves posts from starting date to end date for a particular subreddit for a particular ticker
def get_posts(subreddit, ticker, start, end, size):
    url = f"https://api.pushshift.io/reddit/search/submission/?q={ticker}&subreddit={subreddit}&after={start}&before={end}&size={size}"
    response = requests.get(url)
    return response.json()


# Calculates average daily compound sentiment score for each ticker among multiple posts across multiple subreddits for the past year
def calculate_sentiment_score(subreddits, tickers):
    # Set up default dictionary
    average_daily_sentiment_score = defaultdict(list)

    end = datetime.datetime.now()
    start = end - datetime.timedelta(365)

    for ticker in tickers:
        # Start from one year ago
        current = start
        current_plus_one_day = current + datetime.timedelta(1)

        while current_plus_one_day <= end:
            sum_compound_score = 0
            num_daily_posts = 0

            for subreddit in subreddits:
                # Call get_posts to retrieve posts for this day
                daily_posts = get_posts(subreddit, ticker, int(current.timestamp()), int(current_plus_one_day.timestamp()), 5)

                for post in daily_posts:
                    # Clean each post
                    cleaned2 = cleaning.remove_usernames(cleaning.remove_urls(post))

                    # Calculate sentiment score for each cleaned post
                    sentiment_scores2 = obj.polarity_scores(cleaned2)

                    # For averaging later on
                    sum_compound_score += sentiment_scores2['compound']
                    num_daily_posts += 1

            # Calculate average daily compound sentiment score for this day
            if num_daily_posts > 0:
                average_compound_score = sum_compound_score/num_daily_posts

                # Store date and compound score in dictionary
                average_daily_sentiment_score[ticker].append({'date': current_plus_one_day, 'compound': average_compound_score})

            # Increment to begin calculations for the next period of one day
            current = current_plus_one_day
            current_plus_one_day = current + datetime.timedelta(1)

    return average_daily_sentiment_score

adss = calculate_sentiment_score(subreddits, found_tickers)

# Plot average daily compound sentiment scores on one graph
plt.figure(figsize=(25, 15))

for ticker, data in adss.items():
    dates = [entry['date'] for entry in data]
    compounds = [entry['compound'] for entry in data]
    plt.plot(dates, compounds, label=ticker)

plt.title('Average Daily Compound Sentiment Scores For ')
plt.xlabel('Date')
plt.ylabel('Average Daily Compound Sentiment Score')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()