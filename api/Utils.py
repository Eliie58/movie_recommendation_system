import csv
import re


def readMovies():
    movies = []
    with open('api/resources/movies.csv') as file:
        reader = csv.reader(file, )
        # Skip header
        next(reader, None)
        for row in reader:
            if re.search('\(\d{4}\)', row[1]):
                movies.append({
                    'id': row[0],
                    'title': " ".join(row[1].strip()[:-6].split(",")[::-1]),
                    'year': row[1].strip()[-5:-1],
                    'genres': row[2].split("|")
                })
            else:
                movies.append({
                    'id': row[0],
                    'title': " ".join(row[1].strip().split(",")[::-1]),
                    'year': None,
                    'genres': row[2].split("|")
                })
    return movies
