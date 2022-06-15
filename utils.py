import sqlite3
from collections import Counter


class NetflixConnection:
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()
        self.cursor.close()


def movie_by_title(title):
    netflix_connection = NetflixConnection('netflix.db')

    query = f""" SELECT title, country, release_year, listed_in, description 
           FROM netflix 
           WHERE title LIKE '%{title}%'
           ORDER BY release_year DESC
           LIMIT 1"""
    netflix_connection.cursor.execute(query)
    result = netflix_connection.cursor.fetchone()
    return {
        "title": result[0],
        "country": result[1],
        "release_year": result[2],
        "genre": result[3],
        "description": result[4]
    }


def movies_by_period(year1, year2):
    netflix_connection = NetflixConnection('netflix.db')

    query = f""" SELECT title, release_year
               FROM netflix 
               WHERE release_year BETWEEN {year1} AND {year2}
               LIMIT 100"""
    netflix_connection.cursor.execute(query)
    result = netflix_connection.cursor.fetchall()
    movie_list = []
    for movie in result:
        movie_list.append({"title": movie[0],
                           "release_year": movie[1]})
    return movie_list


def movies_by_rating(rating):
    netflix_connection = NetflixConnection('netflix.db')
    rating_parameters = {
        "children": "'G'",
        "family": "'G', 'PG', 'PG-13'",
        "adult": "'R', 'NC-17'"
    }
    if rating.lower() not in rating_parameters:
        return 'Wrong category. We have only children, adult, family.'
    query = f""" SELECT title, rating, description
               FROM netflix 
               WHERE  rating in ({rating_parameters[rating]})"""
    netflix_connection.cursor.execute(query)
    result = netflix_connection.cursor.fetchall()
    movie_list = []
    for movie in result:
        movie_list.append({"title": movie[0],
                           "rating": movie[1],
                           "description": movie[2]})
    return movie_list


def movies_by_genre(genre):
    netflix_connection = NetflixConnection('netflix.db')

    query = f""" SELECT title, description
               FROM netflix 
               WHERE listed_in LIKE '%{genre}%'
               ORDER BY release_year DESC
               LIMIT 10"""
    netflix_connection.cursor.execute(query)
    result = netflix_connection.cursor.fetchall()
    movie_list = []
    for movie in result:
        movie_list.append({"title": movie[0],
                           "description": movie[1]})
    return movie_list


def movies_by_actors(actor1, actor2):
    netflix_connection = NetflixConnection('netflix.db')

    query = f""" SELECT 'cast'
               FROM netflix 
               WHERE 'cast' LIKE '%{actor1}%' AND 'cast' LIKE '%{actor2}%'"""
    netflix_connection.cursor.execute(query)
    result = netflix_connection.cursor.fetchall()
    actors_list = []
    for cast in result:
        actors_list.extend(cast[0].split(', '))
    counter = Counter(actors_list)
    result_list =[]
    for actor, count in counter.items():
        if actor not in [actor1, actor2] and count>2:
            result_list.append(actor)
    return result_list


def movies_by_type_release_year_genre(type, release_year, genre):
    netflix_connection = NetflixConnection('netflix.db')

    query = f""" SELECT title, description
               FROM netflix 
               WHERE type= '{type}'
               AND release_year = '{release_year}'
               AND listed_in LIKE '%{genre}%'"""
    netflix_connection.cursor.execute(query)
    result = netflix_connection.cursor.fetchall()
    movie_list = []
    for movie in result:
        movie_list.append({"title": movie[0],
                           "description": movie[1]})
    return movie_list


