"""
Module for Utility functions.
"""

import csv
import re
from typing import List


def read_movies() -> List[object]:
    """
    Read movies from resources directory into list of Objects.

    Returns
    -------
    list
        List of movie objects, containing: id, title, year and genre.
    """
    movies = []
    with open('api/resources/movies.csv', encoding='UTF-8') as file:
        reader = csv.reader(file, )
        # Skip header
        next(reader, None)
        for row in reader:
            if re.search('\\(\\d{4}\\)', row[1]):
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
