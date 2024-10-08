import utils.functions as f
import utils.params as p

import requests
import urllib3


def update_db():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    print("Requesting Token...\n")
    res = requests.post(p.auth_url, data=p.payload, verify=False)
    access_token = res.json()["access_token"]

    print("Access Token = {}\n".format(access_token))
    header = {"Authorization": "Bearer " + access_token}

    # The first loop, request_page_number will be set to one, so it requests the first page. Increment this number after
    # each request, so the next time we request the second page, then third, and so on...
    request_page_num = 1
    all_activities = []
    nb_ajout = 0
    upTodate = False

    while not upTodate:
        param = {"per_page": 200, "page": request_page_num}
        # initial request, where we request the first page of activities
        all_activities = f.request(p.activity_url, headers=header, params=param)
        request_page_num += 1
        nb_connues = 0

        # check the response to make sure it is not empty. If it is empty, that means there is no more data left. So if you have
        # 1000 activities, on the 6th request, where we request page 6, there would be no more data left, so we will break out of the loop
        if len(all_activities) == 0:
            upTodate = True

        for i, activity in enumerate(all_activities):
            print(
                "\r Activite {} - {}".format(i + 1, activity["name"]),
                end="",
            )

            if f.is_unknown_activity(activity["id"]):
                activity_infos = {
                    "id": str(activity["id"]),
                    "name": f.formate_str(activity["name"]),
                    "start_date": f.formate_str(activity["start_date"].split("T")[0]),
                    "sport_type": f.formate_str(activity["type"]),
                    "duree": f.get_value(activity, "moving_time", "num"),  # secondes
                    "distance": f.get_value(activity, "distance", "num"),  # metres
                }
                f.add_activity(activity_infos)
                nb_ajout += 1
                nb_connues = 0
            elif nb_connues > 5:
                upTodate = True
            else:
                nb_connues += 1

    p.db_connector.commit()
    print(f"{nb_ajout} nouvelles activités")
    return nb_ajout
