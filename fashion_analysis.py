# -*- coding: utf-8 -*-
"""Fashion Analysis

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YnceQ6Q1KGmfcm2F9TQ01MJyVAr42pC3

Let's see how people feel about Dior's 2023 collection using sentiment analysis tools. We'll use the News API in order to analyze the content from top news outlets, and determine if the fall collection was a flop. Based on some precursory research, it seems that this collection hasn't generated overly positive buzz, but let's see what the numbers say...
"""

!pip install newsapi-python
from newsapi import NewsApiClient
import pandas as pd

newsapi = NewsApiClient(api_key='61893268735d44eb8bba386838c552ce')

API_KEY = "61893268735d44eb8bba386838c552ce"
query = "Christian Dior fall 2023"
positive_articles = 0

endpoint = "https://newsapi.org/v2/everything?q=" + query + "&apiKey=" + API_KEY
response = newsapi.get_everything(q=query)
print(response['articles'])

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('vader_lexicon')
stopwords = set(stopwords.words('english'))

def tokenize_content(content):
  words = nltk.word_tokenize(content)
  words = [word.lower() for word in words if ((word.lower() not in stopwords) and word.isalpha())]
  return words

#Apply tokenization to the current descriptions
article_df = pd.DataFrame.from_dict(response['articles'])

article_df['tokenized'] = article_df['description'].apply(lambda x : tokenize_content(x))
display(article_df)

#start the sentiment analysis
from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
def retrieve_sentiment(content):
  return sia.polarity_scores(content)

#Perform a sentiment analysis to see how people have reacted to Dior's fall 2023
article_df['sentiment'] = article_df['description'].apply(
    lambda x : retrieve_sentiment(x)['compound'])
top_article_df = article_df.sort_values(by='sentiment', ascending=False)
display(top_article_df)
avg_sentiment = top_article_df['sentiment'].mean()
print(avg_sentiment)

"""A score of 0.18 indicates some positive sentiment, however there is not a strong sentiment here. We can take this to mean that Dior's 2023 Fall line has not made a significant impact on news outlets. There are more positive reviews than negative; however, the magnitude is low which means that they weren't overwhelmingly positive. Scanning through some of these articles, we can see that

"""