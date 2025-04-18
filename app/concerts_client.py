import os
import requests
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY")
BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"

def get_concerts(artist_name, cities):
    if not TICKETMASTER_API_KEY:
        raise ValueError("TICKETMASTER_API_KEY not found in environment")

    events = []

    for city in cities:
        params = {
            "apikey": TICKETMASTER_API_KEY,
            "keyword": artist_name,
            "city": city,
            "classificationName": "music",
            "size": 50,  # max per request
        }

        response = requests.get(BASE_URL, params=params)
        data = response.json()

        for event in data.get('_embedded', {}).get('events', []):
            events.append({
                "name": event["name"],
                "date": event["dates"]["start"]["localDate"],
                "city": event["_embedded"]["venues"][0]["city"]["name"],
                "venue": event["_embedded"]["venues"][0]["name"]
            })

    return events


if __name__ == "__main__":

    cities = ["Barcelona", "Madrid", "London"]
    artist = "Kendrick Lamar"

    concerts = get_concerts(artist, cities)
    