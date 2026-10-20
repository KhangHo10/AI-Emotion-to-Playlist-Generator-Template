"""Handles Spotify API queries and playlist creation."""
import random
from functools import lru_cache

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Search query per mood. The music mirrors the detected emotion (sad -> sad music).
# Spotify matches these words against track, artist and album names.
MOODS_QUERY_MAP = {
    "Happy 😄": "feel good happy upbeat pop",
    "Sad 😢": "sad heartbreak acoustic ballad",
    "Angry 😠": "angry rage hard rock metal",
    "Surprised 😲": "euphoric hype dance electronic",
    "Fearful 😨": "dark tense cinematic suspense",
    "Neutral 😐": "chill lofi instrumental focus",
}

SEARCH_PAGE_SIZE = 10  # Development Mode maximum for search
MAX_SEARCH_DEPTH = 60


class SpotifyNotLoggedIn(Exception):
    """No valid Spotify token yet; the login must happen at startup, not inside a web request."""


@lru_cache(maxsize=1)
def get_auth_manager() -> SpotifyOAuth:
    # TODO: Initialize SpotifyOAuth
    return SpotifyOAuth()


def login() -> str:
    # TODO: Login page 


def is_logged_in() -> bool:
    """True if a cached token exists (refreshing it if expired). Never opens a browser."""
    auth = get_auth_manager()
    return auth.validate_token(auth.cache_handler.get_cached_token()) is not None


def get_spotify_client() -> spotipy.Spotify:
    # TODO: Return a Spotify client using the cached auth manager


def _search_tracks(sp: spotipy.Spotify, query: str, limit: int) -> list[dict]:
    """Return `limit` tracks sampled from a random page of the query's top results."""
    first = sp.search(q=query, type="track", limit=SEARCH_PAGE_SIZE)["tracks"]
    items = first["items"]

    # Pick the page from the real result count, so the offset never runs past the end.
    depth = min(first["total"], MAX_SEARCH_DEPTH)
    if depth > SEARCH_PAGE_SIZE:
        offset = random.randint(0, depth - SEARCH_PAGE_SIZE)
        if offset > 0:
            # Spotify's total can overestimate; keep the first page if this one comes back empty.
            items = sp.search(q=query, type="track", limit=SEARCH_PAGE_SIZE, offset=offset)["tracks"]["items"] or items

    items = [t for t in items if t]  # search pages can contain null entries
    return random.sample(items, k=min(limit, len(items)))


def recommend_tracks(mood: str, limit: int = 5) -> list[dict]:
    """Search Spotify for tracks matching the mood. Does not create a playlist."""
    sp = get_spotify_client()

    query = MOODS_QUERY_MAP.get(mood, "pop hits")
    tracks = _search_tracks(sp, query, limit)
    print(f"[spotify] {mood}: query {query!r} -> {len(tracks)} tracks")

    return [
        {
            "name": t["name"],
            "artist": ", ".join(a["name"] for a in t["artists"]),
            "url": t["external_urls"]["spotify"],
            "uri": t["uri"],
            "album_art": t["album"]["images"][-1]["url"] if t["album"]["images"] else None,
        }
        for t in tracks
    ]


def save_playlist(mood: str, track_uris: list[str]) -> dict:
    """Create a private playlist on the user's account with the given tracks."""
    sp = get_spotify_client()
    source = f"Search: '{MOODS_QUERY_MAP.get(mood, 'pop hits')}'"

    # TODO: Create a new private playlist with the mood name and source description, then add the tracks to it.

    sp._post(f"playlists/{playlist['id']}/items", payload={"uris": track_uris})

    return {"id": playlist["id"], "url": playlist["external_urls"]["spotify"]}
