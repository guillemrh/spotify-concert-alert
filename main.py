# main.py

from app.spotify_client import main_loop
from app.concerts_client import get_concerts
from pprint import pprint

def main():
    cities = ["Barcelona", "Madrid", "London"]
    artists = main_loop()

    print(f"Checking concerts for {len(artists)} followed artists...")

    all_concerts = []

    for artist in artists:
        concerts = get_concerts(artist, cities)
        if concerts:
            all_concerts.extend(concerts)
            print(f"💃 {artist}: {len(concerts)} concerts found")
            for concert in concerts:
                print(f"🎤 {artist} is coming to {concert['city']} on {concert['date']} and will play at {concert['venue']}")
    

if __name__ == "__main__":
    main()
