from os.path import dirname, abspath, join
from sqlite3 import connect
import requests
import urllib3
import functions as f
import data.cred as crd

from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# DB params
BASE_DIR = dirname(abspath(__file__))
db_path = join(BASE_DIR, "data", "strava_segments.db")
conn = connect(db_path)
cur = conn.cursor()


# Strava params
auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"
activity_url = "https://www.strava.com/api/v3/activities/"
segment_url = "https://www.strava.com/api/v3/segments/"

payload = crd.payload

print("Requesting Token...\n")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()["access_token"]

print("Access Token = {}\n".format(access_token))
header = {"Authorization": "Bearer " + access_token}

# The first loop, request_page_number will be set to one, so it requests the first page. Increment this number after
# each request, so the next time we request the second page, then third, and so on...
request_page_num = 1
all_activities = []
nb_req = 0
upTodate = False

while not upTodate:
    param = {"per_page": 200, "page": request_page_num}
    # initial request, where we request the first page of activities
    all_activities = f.request(activity_url, headers=header, params=param)
    nb_req += 1
    request_page_num += 1
    nb_connues = 0

    # check the response to make sure it is not empty. If it is empty, that means there is no more data left. So if you have
    # 1000 activities, on the 6th request, where we request page 6, there would be no more data left, so we will break out of the loop
    if len(all_activities) == 0:
        upTodate = True

    for i, activity in enumerate(all_activities):
        print(
            "\r Nb requete = {} // Actvite {} - {}".format(
                nb_req, i + 1, activity["name"]
            ),
            end="",
        )

        if f.is_unknown_activity(activity["id"], cur):
            activity_infos = {
                "id": str(activity["id"]),
                "name": f.formate_str(activity["name"]),
                "start_date": f.formate_str(activity["start_date"].split("T")[0]),
                "sport_type": f.formate_str(activity["type"]),
                "duree": f.get_value(activity, "moving_time", "num"),  # secondes
                "distance": f.get_value(activity, "distance", "num"),  # metres
            }
            f.add_activity(activity_infos, cur)
            nb_connues = 0
        elif nb_connues > 5:
            upTodate = True
        else:
            nb_connues += 1


conn.commit()

year = "2024-01-01"

data = f.retrieve_workout(cur, {"start_date>= ": year, "sport_type=": "Run"})

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame(
    {
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
    }
)

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(
    children=[
        html.H1(children="Hello Dash"),
        html.Div(
            children="""
        Dash: A web application framework for your data.
    """
        ),
        dcc.Graph(id="example-graph", figure=fig),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)


#     param2 = {"include_all_efforts": True}
#     segments = f.request(
#         activity_url + "/" + str(activity["id"]), headers=header, params=param
#     ).get("segment_efforts")
#     nb_req += 1
#     added_segments = cur.execute(
#         """SELECT *
#                                     FROM segments_performances
#                                     WHERE activity_id ={}""".format(
#             activity["id"]
#         )
#     ).fetchall()

#     if len(added_segments) != len(segments):
#         # if 1:
#         for j, seg in enumerate(segments):
#             progress = int(50 * j / len(segments))
#             print(
#                 """\r Nb requete = {} // Actvite {}/{} - {} Traitement des segments : {}""".format(
#                     nb_req,
#                     i + 1,
#                     nb_activities,
#                     activity["name"],
#                     "[" + "=" * progress,
#                 )
#                 + ">" * (progress != 50)
#                 + "-" * (50 - progress)
#                 + "] - "
#                 + str(int(progress / 50 * 100))
#                 + "%",
#                 end="",
#             )
#             if f.is_unknown_segment(seg["segment"]["id"], cur):

#                 segment_elevation_gain = f.get_value(
#                     f.request(
#                         segment_url + "/" + str(seg["segment"]["id"]),
#                         headers=header,
#                     ),
#                     "total_elevation_gain",
#                     "num",
#                 )
#                 nb_req += 1

#                 segment_infos = {
#                     "id": f.get_value(seg["segment"], "id", "num"),
#                     "name": f.get_value(seg, "name", "str"),
#                     "distance": f.get_value(seg, "distance", "num"),
#                     "total_elevation_gain": segment_elevation_gain,
#                     "maximum_grade": f.get_value(
#                         seg["segment"], "maximum_grade", "num"
#                     ),
#                     "average_grade": f.get_value(
#                         seg["segment"], "average_grade", "num"
#                     ),
#                     "city": f.get_value(seg["segment"], "city", "str"),
#                     "state": f.get_value(seg["segment"], "state", "str"),
#                     "country": f.get_value(seg["segment"], "country", "str"),
#                 }
#                 f.create_segment(segment_infos, cur)

#             perf_infos = {
#                 "segment_id": f.get_value(seg["segment"], "id", "num"),
#                 "activity_id": f.get_value(activity, "id", "num"),
#                 "elapsed_time": f.get_value(seg, "elapsed_time", "num"),
#                 "average_speed": f.get_value(
#                     seg, ["distance", "elapsed_time"], "speed"
#                 ),
#                 "average_watts": f.get_value(seg, "average_watts", "num"),
#                 "average_heartrate": f.get_value(seg, "average_heartrate", "num"),
#                 "max_heartrate": f.get_value(seg, "max_heartrate", "num"),
#                 "start_date": f.get_value(seg, "start_date", "str"),
#                 "activity_type": f.get_value(
#                     seg["segment"], "activity_type", "str"
#                 ),
#             }
#             f.add_perf(perf_infos, cur)

#     conn.commit()

#     # f.add_perf(seg)

#     # perf = {'elapsed_time': seg['elapsed_time'],
#     #         'average_speed': round(seg['distance']/seg['elapsed_time']*3.6, 1),
#     #         'average_watts': seg['average_watts'],
#     #         'average_heartrate': seg['average_heartrate']
#     #         }
#     # if segments_history.get(seg["id"]):
#     #     """
#     #     A réfléchir au passage avec une BDD
#     #     Si déjà passé par le segment :
#     #             - trouver un ID pour ce passage (gérer les cas de plusieurs passage par ride)
#     #             - insérer dans l'historique
#     #             - incrémenter le compteur de passage du dictionnaire des infos de passage
#     #     sinon :
#     #             - insérer un nouveau segment exploré dans les 2 dictionnaires
#     #             - ajouter la performance à l'historique
#     #     """
#     # segments_history[seg["id"]] = perf
