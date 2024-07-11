import praw
import cleaning
import tickers
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

found_tickers = []

for subreddit in subreddits:
    # Fetch submissions for each subreddit
    for submission in reddit.subreddit(subreddit).hot(limit=20):
        cleaned = cleaning.remove_urls(submission.selftext)
        found_tickers.extend(tickers.find_tickers(cleaned))

print(found_tickers)
