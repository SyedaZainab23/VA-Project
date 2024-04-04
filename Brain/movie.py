import http.client
import json
import re

movie_keywords_list = ['movie', 'series', 'shows', 'entertainment', 'watch', 'top']

def get_movie_details(input_text):
    conn = http.client.HTTPSConnection("imdb-top-100-movies.p.rapidapi.com")
    number_match = re.search(r'\b(\d+)\b', input_text)

    if number_match:
        number = number_match.group(1)
        result = "/top" + number
    else:
        result =""
    headers = {
        'X-RapidAPI-Key': "43c346e996msh4cba67d7a1ab72bp122062jsn58851784a0ce",
        'X-RapidAPI-Host': "imdb-top-100-movies.p.rapidapi.com"
    }

    conn.request("GET", result, headers=headers)

    res = conn.getresponse()
    data = res.read()

    # Decode the data
    dd = data.decode("utf-8")

    # Parse JSON string into a Python dictionary
    data_dict = json.loads(dd)
    if number_match:
        return data_dict['title']
    else:
        return [movie['title'] for movie in data_dict]

# Example usage:
#topMovies = get_movie_details("get me 2 top movies")
#print(topMovies)
