# -*- coding: utf-8 -*-
"""project1_Moody.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Cd6Wn_Zu3fr84_B3Vom2nVBBCpII-y-l

# Project 1
## Jada Moody
### 3/1/2023
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv('https://drive.google.com/uc?export=download&id=18t5IYN05Oh6mfNvyW5KhUgdCgt5eZUfq')
df.head()

df.info()

df.nunique()

df.describe()

"""#Dropping columns"""

df = df.drop(['sid', 'store_url', 'name', 'description'], axis=1)

"""I decided to drop the sid column because it's an id columns and isn't really relavent to the data analysis.

#Duplicate rows
"""

dup_mask = df.duplicated()
print(f'There are {dup_mask.sum()} duplicates')

df.info()

"""#Missing Values"""

mask = df['full_price'] == 'free'
print(mask.sum())

df['full_price'] = df['full_price'].replace('free', 0)
df['full_price'] = pd.to_numeric(df['full_price'])

"""I figured out that full_price had a data type of object so I tried to convert to numeric but it had some string values so I had to replace those string values "free" with 0."""

df.info()

df.info()

df.head()

df = df.dropna(subset=['published_store'])

df['published_store'] = pd.to_datetime(df['published_store'])

"""I dropped the NaN rows since there weren't a lot and converted the data type to datetime"""

df.info()

df.info()

df[df['discount'].isna()]

df['discount'] = df['discount'].fillna(0)

"""Decided to fill the NaN with 0 since 0 wouldn't effect the data or calculation that come with it"""

df.info()

df = df.dropna(subset=['languages'])

"""I drop the NaN from both since there weren't a lot and wouldn't make a big difference"""

df.info()

df['gfq_difficulty'] = df['gfq_difficulty'].fillna("unknown")

"""Decided to fill the NaN with unknown since this was an object data type"""

df.info()

df.isna().sum() / df.shape[0]

df = df.dropna(subset=['store_uscore'])

"""Determined that it would be okay to drop the NaN from this column"""

med2 = df['gfq_length'].median()
df['gfq_length'] = df['gfq_length'].fillna(med2)

"""Decided to fill the NaN with the median, didn't really know another value to fill with"""

df.info()

"""#Ordinal encoding"""

df['gfq_difficulty'].unique()

ord_map = {
    "Simple": 1,
    "Simple-Easy": 2,
    "Easy": 3,
    "Easy-Just Right": 4,
    "Just Right": 5,
    "Just Right-Tough": 6,
    "Tough": 7,
    "Tough-Unforgiving": 8,
    "Unforgiving": 9,
    "unknown": 10


}

df['gfq_difficulty'] = df['gfq_difficulty'].map(ord_map)

df

"""#Discretization"""

out, bins = pd.cut(df['stsp_owners'], bins=3,
        labels=['1', '2', '3'], retbins=True)

"""#Multiple-value columns"""

df['windows'] = 0
df['mac'] = 0
df['linux'] = 0

for index, row in df.iterrows():
    platforms = row['platforms'].split(',')
    for platform in platforms:
        if platform == 'WIN':
            df.loc[index, 'windows'] = 1
        elif platform == 'MAC':
            df.loc[index, 'mac'] = 1
        elif platform == 'LNX':
            df.loc[index, 'linux'] = 1


df = df.drop('platforms', axis=1)

"""This is not the same as one-hot enconding"""

def count_languages(lang_str):
    return lang_str.count(',') + 1


df["languages"] = df["languages"].apply(count_languages)

df["languages"] = pd.to_numeric(df["languages"])

df.head()

"""#New price column"""

df["price"] = (df["full_price"] - df["discount"]) / 100

df = df.drop(['full_price', 'discount'], axis=1)

df.describe()

"""#Price outliers"""

fig, ax = plt.subplots()
df['price'].plot(kind='hist', bins=12, ax=ax)
ax.set_xlabel('price')
ax.set_ylabel('Frequency')
ax.set_title('Histogram')

df = df.loc[df['price'] < 50]

df.describe()

"""I decided to make a histogram to note the outliers. I don't think that there are any outliers in this data

#Normalize ratings
"""

score_min = df['store_uscore'].min()
score_max = df['store_uscore'].max()
score_range = score_max - score_min
df['store_uscore'] = (df['store_uscore'] - score_min) / score_range

df

rating_min = df['gfq_rating'].min()
rating_max = df['gfq_rating'].max()
rating_range = rating_max - rating_min
df['gfq_rating'] = (df['gfq_rating'] - rating_min) / rating_range

df

"""#New age column"""

df['age'] = 2023 - df['published_store'].dt.year

df.head()

"""#Making visulizations"""

fig, ax = plt.subplots()
df['languages'].plot(kind='hist', bins=5, ax=ax)
ax.set_xlabel('Number of languages')
ax.set_ylabel('Frequency')
ax.set_title('Histogram of languages')

fig, ax = plt.subplots()
df['price'].plot(kind='hist', bins=5, ax=ax)
ax.set_xlabel('Price')
ax.set_ylabel('Frequency')
ax.set_title('Histogram of prices')

fig, ax = plt.subplots()
gfq_difficulty_counts = df["gfq_difficulty"].value_counts()
gfq_difficulty_counts.plot(kind="bar", ax=ax)
ax.set_title("Difficulty of games")
ax.set_xlabel("Difficulty")
ax.set_ylabel("Number of Games")

fig, ax = plt.subplots()
age_counts = df["age"].value_counts()
age_counts.plot(kind="bar", ax=ax)
ax.set_title("Age of games")
ax.set_xlabel("Age")
ax.set_ylabel("Number of Games")

platform_totals = df[["windows", "mac", "linux"]].sum()

fig, ax = plt.subplots()
platform_totals.plot(kind="bar")
ax.set_title("Total Games by Platform")
ax.set_xlabel("Platform")
ax.set_ylabel("Number of Games")

"""#Making correlation matrix"""

corr_mat = df.corr()

fig, ax = plt.subplots(figsize=(10, 10))

sns.heatmap(corr_mat, square=True, annot=True, fmt='.2f', cbar=True, cmap="coolwarm", ax=ax)

ax.set_title('Correlation')

"""The top 5 correlations are:
1. mac and linux - the games are likely to have operate with these platforms.
2. gfq_length and price - the length of the game can determine how much a game costs.
3. store_uscore and gfq_rating - the rating the user gives a game has a relationship on the average score that the user obtained.  
4. gfq_length and gfq_rating - The length of the game has some affect of the user's rating of the game.  
5. languages and price - The number of languges and types of languages have some affect on the price of the game.

#Making scatter plot
"""

df.head()

fig, ax = plt.subplots(figsize = (10, 10))
ax.scatter(x=df['store_uscore'], y=df['gfq_rating'], alpha=0.05, c='green')
ax.set_xlabel('score')
ax.set_ylabel('rating')
ax.set_title('Score vs Rating');

"""The two variables have a correlation coefficient of 0.24, meaning that they have some correlation which is shown in the graph. The dots are going up towards the right. It's not a strong correlation but there is a correlation.

#Making bar chart
"""

genre_prices = df.groupby('genre')['price'].mean()

genre_prices = genre_prices.sort_values(ascending=False)

fig, ax = plt.subplots()
genre_prices.plot(kind='bar', ax=ax)
ax.set_xlabel('Genre')
ax.set_ylabel('Average Price')
ax.set_title('Average Price of Games by Genre')

"""#New visulization"""

mask = df['age'] >= 15
grouped = df[mask].groupby('genre')['gfq_length'].mean()

grouped.plot(kind='bar')

"""I used a mask to get the games that had an age greater than or equal to 15. I preformed a groupby on that mask to get the average length of games for each genre that has an age greater than or equal to 15."""

