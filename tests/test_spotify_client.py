import pytest
from unittest.mock import patch, MagicMock
import sys, os

from app.spotify_client import authenticate_spotify, get_followed_artists

@patch("app.spotify_client.SpotifyOAuth.get_access_token")
@patch("app.spotify_client.spotipy.Spotify")
def test_authenticate_spotify_success(mock_spotify, mock_get_access_token):
    mock_get_access_token.return_value = {"access_token": "test_token"}
    sp = authenticate_spotify()
    mock_spotify.assert_called_once()
    assert sp is not None

import spotipy

@patch("app.spotify_client.SpotifyOAuth", side_effect=spotipy.exceptions.SpotifyException(400, -1, "Auth failed"))
def test_authenticate_spotify_spotify_exception(mock_spotify_oauth):
    with pytest.raises(spotipy.exceptions.SpotifyException):
        from app.spotify_client import authenticate_spotify
        authenticate_spotify()
        
@patch("app.spotify_client.SpotifyOAuth.__init__", return_value=None)
@patch("app.spotify_client.spotipy.Spotify")
def test_authenticate_spotify_failure(mock_spotify, mock_init):
    mock_spotify.side_effect = ValueError("No token available")
    with pytest.raises(ValueError):
        authenticate_spotify()
        
def test_missing_spotify_credentials():
    with patch.dict(os.environ, {"SPOTIFY_CLIENT_ID": "", "SPOTIFY_CLIENT_SECRET": "", "SPOTIFY_REDIRECT_URI": ""}):
        # Reload the module to re-trigger the global variable loading logic
        with pytest.raises(EnvironmentError) as excinfo:
            # Delayed import so it picks up the patched env
            import importlib
            from app import spotify_client
            importlib.reload(spotify_client)

        assert "Spotify credentials not found in environment variables." in str(excinfo.value)        
        
@patch("app.spotify_client.spotipy.Spotify.current_user_followed_artists")
def test_get_followed_artists_success(mock_followed):
    mock_followed.side_effect = [
        {"artists": {"items": [{"name": "Artist1", "id": "1", "genres": ["pop"], "popularity": 80}]}},
        {"artists": {"items": []}},
    ]
    sp = MagicMock()
    sp.current_user_followed_artists = mock_followed
    result = get_followed_artists(sp)

    assert len(result) == 1
    assert result[0]["name"] == "Artist1"

@patch("app.spotify_client.spotipy.Spotify.current_user_followed_artists", side_effect=spotipy.exceptions.SpotifyException(500, -1, "API error"))
def test_get_followed_artists_spotify_exception(mock_followed):
    sp = patch("app.spotify_client.spotipy.Spotify").start().return_value
    sp.current_user_followed_artists = mock_followed
    with pytest.raises(spotipy.exceptions.SpotifyException):
        from app.spotify_client import get_followed_artists
        get_followed_artists(sp)

@patch("app.spotify_client.spotipy.Spotify.current_user_followed_artists")
def test_get_followed_artists_failure(mock_followed):
    mock_followed.side_effect = Exception("API error")
    sp = MagicMock()
    sp.current_user_followed_artists = mock_followed

    with pytest.raises(Exception):
        get_followed_artists(sp)

from unittest.mock import patch

@patch("app.spotify_client.authenticate_spotify", side_effect=RuntimeError("Boom"))
@patch("app.spotify_client.logger")
def test_main_loop_error_handling(mock_logger, mock_auth):
    from app.spotify_client import main_loop
    main_loop()
    
    # Check that the error was logged
    mock_logger.error.assert_called_with("Error in main process: Boom")

@patch("app.spotify_client.authenticate_spotify")
@patch("app.spotify_client.get_followed_artists")
@patch("app.spotify_client.logger")
def test_main_loop_logs_artists(mock_logger, mock_get_artists, mock_auth):
    from app.spotify_client import main_loop

    mock_auth.return_value = MagicMock()
    mock_get_artists.return_value = [{"name": "Artist One"}, {"name": "Artist Two"}]

    main_loop()

    mock_logger.info.assert_any_call(" - Artist One")
    mock_logger.info.assert_any_call(" - Artist Two")