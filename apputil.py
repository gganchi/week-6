# your code here ...

import requests
import pandas as pd


class Genius:
    """
    Creating a class to interact with the Genius API.
    """

    def __init__(self, access_token):
        """
        Initialize the Genius object with an access token.
        """
        self.access_token = access_token
        self.base_url = "https://api.genius.com"
        self.headers = {"Authorization": f"Bearer {self.access_token}"}

    def get_artist(self, search_term):
        """
        Retrieve artist information for the first search hit.
        """
        # Search the Genius API using the provided term
        search_url = f"{self.base_url}/search"
        response = requests.get(
            search_url,
            headers=self.headers,
            params={"q": search_term},
            timeout=10
        )
        response.raise_for_status()
        json_data = response.json()

        # Extract the first matching artist ID (if any)
        hits = json_data.get("response", {}).get("hits", [])
        if not hits:
            return {}

        artist_id = hits[0]["result"]["primary_artist"]["id"]

        # Use the artist ID to fetch detailed artist information
        artist_url = f"{self.base_url}/artists/{artist_id}"
        artist_response = requests.get(
            artist_url,
            headers=self.headers,
            timeout=10
        )
        artist_response.raise_for_status()
        return artist_response.json()

    def get_artists(self, search_terms):
        """
        Retrieve artist information for multiple search terms.
        """
        # Loop through all search terms, collect artist details,
        # and store them in a list of dictionaries
        rows = []
        for term in search_terms:
            data = self.get_artist(term)

            if not data:
                rows.append({
                    "search_term": term,
                    "artist_name": None,
                    "artist_id": None,
                    "followers_count": None
                })
                continue

            artist_obj = data.get("response", {}).get("artist", {})
            rows.append({
                "search_term": term,
                "artist_name": artist_obj.get("name"),
                "artist_id": artist_obj.get("id"),
                "followers_count": artist_obj.get("followers_count")
            })

        # Convert collected data into a DataFrame for easy analysis
        return pd.DataFrame(rows)