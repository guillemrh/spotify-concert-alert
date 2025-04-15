import os
import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth, CacheFileHandler
from dotenv import load_dotenv
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
SCOPE = "user-follow-read"

if not CLIENT_ID or not CLIENT_SECRET or not REDIRECT_URI:
    logger.error("Spotify credentials (CLIENT_ID, CLIENT_SECRET, REDIRECT_URI) are not set.")
    raise EnvironmentError("Spotify credentials not found in environment variables.")

def authenticate_spotify():
    """Authenticate with Spotify and return the Spotify API client."""
    try:
        logger.info("Authenticating with Spotify...")
        cache_handler = CacheFileHandler(cache_path="/spotify_client/app/.cache")
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=SCOPE,
            cache_handler=cache_handler
        ))
        logger.info("Authentication successful.")
        return sp
    except spotipy.exceptions.SpotifyException as e:
        logger.error(f"Spotify API error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during authentication: {e}")
        raise

def get_followed_artists(sp, limit=50):
    """Fetch followed artists with error handling."""
    artists = []
    after = None

    try:
        while True:
            response = sp.current_user_followed_artists(limit=limit, after=after)
            items = response['artists']['items']
            if not items:
                break
            artists.extend(items)
            after = items[-1]['id']
        logger.info(f"Retrieved {len(artists)} followed artists.")
        return [
            {
                "name": artist["name"],
                "id": artist["id"],
                "genres": artist["genres"],
                "popularity": artist["popularity"]
            }
            for artist in artists
        ]
    except spotipy.exceptions.SpotifyException as e:
        logger.error(f"Spotify API error while fetching artists: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while fetching artists: {e}")
        raise

def main_loop(sleep_duration=1):
    """
    Main loop to authenticate with Spotify, fetch followed artists, and log their names.
    :param sleep_duration: Time to sleep between iterations (in seconds).
    """
    print("Running Spotify Client...")
    try:
        sp = authenticate_spotify()
        artists = get_followed_artists(sp)
        for artist in artists:
            logger.info(f" - {artist['name']}")
    except Exception as e:
            logger.error(f"Error in main process: {e}")
    finally:
            logger.info(f"Sleeping for {sleep_duration} seconds...")
            time.sleep(sleep_duration)
        
if __name__ == "__main__":
    main_loop() # pragma: no cover

