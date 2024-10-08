from os.path import dirname, abspath, join
from sqlite3 import connect
from data.cred import client_secret, refresh_token

# DB params
BASE_DIR = dirname(dirname(abspath(__file__)))
db_path = join(BASE_DIR, "data", "strava_segments.db")
db_connector = connect(db_path)
db_cursor = db_connector.cursor()


# Strava params
auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"
activity_url = "https://www.strava.com/api/v3/activities/"
segment_url = "https://www.strava.com/api/v3/segments/"

payload = {
    "client_id": "105271",
    "client_secret": client_secret,
    "refresh_token": refresh_token,
    "grant_type": "refresh_token",
    "f": "json",
}
