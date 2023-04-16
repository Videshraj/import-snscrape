import os

os.system('pip install snscrape')
os.system('pip install pandas')
os.system('pip install pymongo')
os.system('pip install streamlit')
import snscrape
import pandas as pd
from pymongo import MongoClient
import streamlit as st

# Function to scrape Twitter data using snscrape library
def scrape_twitter_data(keyword, start_date, end_date, limit):
    # Initialize an empty list to store scraped data
    tweets = []
    # Set up the snscrape query
    query = f'{keyword} since:{start_date} until:{end_date}'
    for tweet in snscrape.TwitterSearchScraper(query).get_items():
        if len(tweets) >= limit:
            break
        tweet_data = {
            'date': tweet.date,
            'id': tweet.id,
            'url': tweet.url,
            'content': tweet.content,
            'user': tweet.user.username,
            'reply_count': tweet.replyCount,
            'retweet_count': tweet.retweetCount,
            'language': tweet.lang,
            'source': tweet.sourceUrl,
            'like_count': tweet.likeCount
        }
        tweets.append(tweet_data)
    return tweets

# Function to store scraped data into MongoDB
def store_data_in_mongodb(data, keyword):
    # Connect to MongoDB
    client = MongoClient('mongodb+srv://vradmin:vpreCR8304@cluster0.dpqqowe.mongodb.net/test')
    db = client['twitter_db']
    collection = db[keyword]
    # Insert data into MongoDB
    collection.insert_many(data)
    # Close MongoDB connection
    client.close()

# Streamlit GUI for user interaction
def run_streamlit_app():
    st.title('Twitter Scraping')
    # Get user input for keyword, date range, and limit
    keyword = st.text_input('Enter keyword or hashtag to be searched:')
    start_date = st.date_input('Select start date:')
    end_date = st.date_input('Select end date:')
    limit = st.number_input('Enter limit for tweet count:', min_value=1, max_value=1000, step=1)
    # Scrape data on button click
    if st.button('Scrape Twitter Data'):
        tweets = scrape_twitter_data(keyword, start_date, end_date, limit)
        # Display scraped data in a dataframe
        if len(tweets) > 0:
            df = pd.DataFrame(tweets)
            st.dataframe(df)
            # Store data in MongoDB on button click
            if st.button('Upload Data to MongoDB'):
                store_data_in_mongodb(tweets, keyword)
                st.success('Data uploaded to MongoDB successfully!')
        else:
            st.warning('No data found for the given keyword and date range.')

# Run the Streamlit app
if __name__ == '__main__':
    run_streamlit_app()