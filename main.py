import praw
import pymongo

import src.cleaning as cleaning
import src.tickers as tickers
from dotenv import load_dotenv
import os

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

found_tickers = []

for subreddit in subreddits:
    # Fetch submissions for each subreddit
    for submission in reddit.subreddit(subreddit).hot(limit=20):
        cleaned = cleaning.remove_usernames(cleaning.remove_urls(submission.selftext))
        found_tickers.extend(tickers.find_tickers(cleaned))

        # Store the data of the posts
        post_data = {
            'title': submission.title,
            'content': cleaned,
            'timestamp': submission.created_utc,
            'subreddit': subreddit,
            # 'ticker': tickers_in_post
        }
        collection.insert_one(post_data)

print("TICKERS FOUND: ", found_tickers)
