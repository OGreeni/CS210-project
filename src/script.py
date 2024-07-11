import praw
import cleaning

# List of subreddits to use
subreddits = ["Investing", "StockMarket", "Stocks", "Trading"]

# Create a reddit client
reddit = praw.Reddit(
    client_id="CLIENT_ID",
    client_secret="CLIENT_SECRET",
    user_agent="USER_AGENT"
)

for subreddit in subreddits:
    # Fetch submissions for each subreddit
    for submission in reddit.subreddit(subreddit).hot(limit=20):
        print(submission.title)
        print(submission.selftext)
