import pandas as pd

"""
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
"""

unames=["user_id","gender","age","occupation","zip"]

users = pd.read_table(
    "datasets/movielens/users.dat", 
    sep="::",
    header=None,
    engine="python",
    names=unames
)

rnames=["user_id","movie_id","rating","timestamp"]

ratings = pd.read_table(
    "datasets/movielens/ratings.dat", 
    sep="::",
    header=None,
    engine="python",
    names=rnames
)

mnames=["movie_id","title","genres"]

movies = pd.read_table(
    "datasets/movielens/movies.dat", 
    sep="::",
    header=None,
    engine="python",
    names=mnames
)

data = pd.merge(pd.merge(ratings, users), movies)

mean_ratings = data.pivot_table(
        values="rating", 
        index="title",
        columns="gender",
        aggfunc="mean"
    )


ratings_by_title = data.groupby("title").size()

active_titles = ratings_by_title.index[ratings_by_title >= 250]

mean_ratings = mean_ratings.loc[active_titles]

#a las mujeres les gusta mas close shave
#print(mean_ratings.sort_values(by="F", ascending=False))

mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']

#print(mean_ratings)

sorted_by_diff = mean_ratings.sort_values(by="diff")

#print(sorted_by_diff[::-1])


rating_std_by_title = data.groupby("title")["rating"].std()

rating_std_by_title = rating_std_by_title.loc[active_titles]

#print(rating_std_by_title.sort_values(ascending=False)[:10])


movies["genre"] = movies.pop("genres").str.split("|")

movies_exploded = movies.explode("genre")

#print(ratings)

ratings_by_genre = pd.merge(
    pd.merge(
        movies_exploded, 
        ratings
    ), 
    users
)

print(
    ratings_by_genre.
    groupby(["genre","age"])['rating'].mean().
    unstack("age")
      )



