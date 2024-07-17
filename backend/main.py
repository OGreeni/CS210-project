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
import yfinance as yf  
import pandas as pd  
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression 
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.metrics import mean_squared_error 
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Load env variables from .env
load_dotenv()

# Initialize analyzer
obj = SentimentIntensityAnalyzer()

# Create a reddit client
reddit = praw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    user_agent=os.getenv('USER_AGENT')
)

# Set up MongoDB connection
client = pymongo.MongoClient(os.getenv('MONGODB_URI'))
db = client.reddit_data
posts_coll = db.posts
avg_sentiments_coll = db.average_sentiments

# Delete any existing data from previous runs
# posts_coll.drop()
# avg_sentiments_coll.drop()

# Set up default dictionary
sentiment_dict = defaultdict(list)

# List of subreddits to use
subreddits = ["Investing", "StockMarket", "Stocks", "Trading"]

found_tickers = []

for subreddit in subreddits:
    # Fetch submissions for each subreddit
    for submission in reddit.subreddit(subreddit).hot(limit=1000):
        cleaned = cleaning.remove_usernames(cleaning.remove_urls(submission.selftext))
        submission_tickers = tickers.find_tickers(cleaned)  # Stores tickers found in each cleaned submission

        if len(submission_tickers) == 0:
            continue

        found_tickers.extend(submission_tickers)

        # Calculate sentiment scores (including compound, pos, neu, neg) of the cleaned data
        sentiment_scores = obj.polarity_scores(cleaned)

        # Use compound score to determine whether the content is positive, negative, or neutral
        sentiment = 'positive' if sentiment_scores['compound'] >= 0.1 \
            else 'negative' if sentiment_scores['compound'] <= -0.1 \
            else 'neutral'

        # Append the sentiment scores for each ticker found in the submission
        for ticker in submission_tickers:
            sentiment_dict[ticker].append(sentiment_scores)

        # Store the data of the post
        post_data = {
            'timestamp': submission.created_utc,
            'tickers': submission_tickers,
            'sentiment': sentiment_scores['compound'],
        }
        posts_coll.insert_one(post_data)

avg_sentiments = {}

# Averages sentiment scores across all submissions for each ticker
for ticker, sentiments in sentiment_dict.items():
    average_sentiment = {
        'compound': np.mean([s['compound'] for s in sentiments]),
        'pos': np.mean([s['pos'] for s in sentiments]),
        'neu': np.mean([s['neu'] for s in sentiments]),
        'neg': np.mean([s['neg'] for s in sentiments]),
        'count': len(sentiments)  # Number of submissions
    }
    avg_sentiments[ticker] = average_sentiment

# Store the averages in a MongoDB collection
for ticker, average_sentiment in avg_sentiments.items():
    avg_sentiments_coll.insert_one({
        'ticker': ticker,
        'averageSentiment': average_sentiment
    })

# Set up start and end dates
start_date = (datetime.now() - timedelta(5)).strftime('%Y-%m-%d')
end_date = datetime.now().strftime('%Y-%m-%d')

# Get past stock price data
stock_price = {}
for ticker in avg_sentiments.keys():
    ticker_data = yf.download(ticker, start_date, end_date)
    stock_price[ticker] = ticker_data

# Set up dataframe with stock price and related information
dataset = []
for ticker, prices in stock_price.items():
    for date, row in prices.iterrows():
        date_str = date.strftime('%Y-%m-%d')
        if date_str in avg_sentiments:
            dataset.append([
                ticker,
                date,
                avg_sentiments[ticker]['compound'],
                row['Price']
            ])
df = pd.DataFrame(dataset, columns=['ticker', 'date', 'compound', 'price'])

# Set up dataset and target variable
X = df[['compound']]
Y = df['price']

# Split up dataset intro training and testing set, train model
X_training_set, X_testing_set, Y_training_set, Y_testing_set = train_test_split(X, Y, 0.2, 1)

predictive_model = LinearRegression()
predictive_model.fit(X_training_set, Y_training_set)

# Calculate MSE, RMSE, and r^2 of predicted and actual stock price
Y_predicted = predictive_model.predict(X_testing_set)

mse = mean_squared_error(Y_testing_set, Y_predicted)
print('Mean Squared Error: ' + str(mse))

rmse = mean_squared_error(Y_testing_set, Y_predicted, squared=False)
print('Root Mean Squared Error: ' + str(rmse))

r2 = r2_score(Y_testing_set, Y_predicted)
print('R-squared: ' + str(r2))

# Plot actual stock prices with the model's predicted stock prices for each ticker we found
for ticker in tickers:
    # Get the actual and predicted values of the stock prices of each ticker
    Y_testing_set_ticker = Y_testing_set[ticker]
    Y_predicted_ticker = Y_predicted[ticker]
    
    # Create a plot for each ticker
    plt.figure(figsize=(15, 10))
    plt.plot(Y_testing_set_ticker.values, 'Actual Stock Price')
    plt.plot(Y_predicted_ticker, 'Predicted Stock Price')
    plt.title('Actual vs Predicted Stock Prices for ' + ticker)
    plt.xlabel('Time in Days')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.show()

