# 🎧 Spotify Concert Alert

Get notified when an artist you follow on Spotify announces a concert in one of your favorite cities.

## 🚀 Project Goal

Automatically check for new concerts from the artists you follow on Spotify, filter them by a list of cities you define, and send you a notification when a relevant event is detected.

## 🛠️ Tech Stack

- Python 3.10+
- Docker & Docker Compose
- [Spotipy](https://spotipy.readthedocs.io/) (Spotify Web API)
- Songkick API (for concert data)
- Telegram Bot (for push notifications)
- `.env` for secrets and environment configuration

## 📁 Project Structure
```
spotify-concert-alert/
│
├── app/
│   ├── __init__.py
│   ├── spotify_client.py     # Logic for authentication and Spotify queries
│   ├── concerts_client.py    # Logic to fetch concert data (e.g., Songkick)
│   ├── notifier.py           # Send notifications (email, Telegram, etc.)
│   └── config.py             # Load environment variables
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml    # Configuration for Docker services
│
├── .env                      # Environment variables (API keys, etc.)
├── .gitignore                
├── README.md                 
├── requirements.txt          
└── schedule.py               # Script to define task scheduling
```