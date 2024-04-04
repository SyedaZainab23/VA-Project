import http.client
import json
from load_key_from_config import getConfigKey

news_keywords_list = ["latest", "world", "Business", "health", "sport", "science", "technology"]
language="en-US"

def processNewsRequest(userinput):
    for keyword in news_keywords_list:
        if keyword.lower() in userinput:
            endpoint='/'+keyword
    api_key = getConfigKey("newsAPI")
    conn = http.client.HTTPSConnection("google-news13.p.rapidapi.com")
    headers = {
        'X-RapidAPI-Key': api_key,
        'X-RapidAPI-Host': "google-news13.p.rapidapi.com"
    }
    conn.request("GET", f"{endpoint}?lr={language}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data)

    # Extract titles of the news articles
    titles = [item['title'] for item in data['items']]
    return titles

# Example usage:
#news_latest = processNewsRequest("what is todays world news")  # Get latest news

#print("Latest News:")
#print(news_latest)
