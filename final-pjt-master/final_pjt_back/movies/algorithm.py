import json 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

def recommend(data):
    print('오라오라오라오라')
    me = data['me']
    df_me = pd.DataFrame([list(me.values())], columns=me.keys())
    others = data['others']
    movies = data['movies']
    
    df_others = pd.DataFrame(others)
    df_movies = pd.DataFrame(movies)
    df_me.drop(df_me.columns[[0,1,3,4,5]], axis=1, inplace=True)
    df_others.drop(df_others.columns[[0,1,3,4,5]], axis=1, inplace=True)
    df_movies.drop(df_movies.columns[[1,2,3,5,7,8,9]], axis=1, inplace=True)
    # print(df_movies.columns)
    # print(df_movies.head())
    like_movies_ids = df_me['like_movies'].values[0]  # like_movies 열의 값을 가져옴
    print(df_me['like_movies'].values[0])
    genre_counts = Counter()
    for movie_id in like_movies_ids:
        genres = df_movies.loc[df_movies['id'] == movie_id, 'genre_ids'].values[0]
        genre_counts.update(genres)

    genres = list(genre_counts.keys())
    counts = list(genre_counts.values())
    # print(username)
    others_like_list = {}
    print(df_others)
    for index, row in df_others.iterrows():
        user_name = row['username']
        others_like_movies = row['like_movies']
        others_like_list[user_name] = others_like_movies
    
    score = {}
    for othername, movies in others_like_list.items():
        score[othername] = 0
        for movie in movies:
            if movie in like_movies_ids:
                score[othername] += 1
    score_items = sorted(score.items(), key=lambda x: x[1], reverse=True)
    top3 = score_items[:5]
    # genres = df_movies.loc[df_movies['id'] == movie_id, 'genre_ids'].values[0]
    print(top3)
    recommend_list = []
    for name, rate in top3:
        print(name)
        movies = df_others.loc[df_others['username']==name, 'like_movies'].values[0]
        # print('111111111111111111111111111111111',movies)
        recommend_list.extend(movies)
    
    recommend_list = set(recommend_list)
    like_movies_ids = set(like_movies_ids)
    # print('==================================',recommend_list)
    recommend_list = list(recommend_list-like_movies_ids)
    
    # print('------------------------',genre_counts)
    
    # plt.bar(range(len(genres)), counts, align='center')
    # plt.xticks(range(len(genres)), genres)
    # plt.xlabel('Genre')
    # plt.ylabel('Count')
    # plt.title('Genre Counts')

    # # 그래프 출력
    # plt.show()

    return recommend_list, genre_counts

