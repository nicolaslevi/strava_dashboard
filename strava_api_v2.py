import utils.functions as f
import utils.params as p

import urllib3
import requests


def disable_ssl_warnings():
    """Désactive les avertissements liés aux certificats SSL."""
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_access_token(auth_url, payload):
    """Récupère un jeton d'accès via une requête POST."""
    try:
        response = requests.post(auth_url, data=payload, verify=False)
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.RequestException as e:
        raise RuntimeError(f"Erreur lors de la récupération du token : {e}")


def fetch_activities_page(url, headers, page):
    """Récupère une page d'activités."""
    params = {"per_page": 200, "page": page}
    return f.request(url, headers=headers, params=params)


def process_activity(activity):
    """Formate et retourne les informations d'une activité."""
    return {
        "id": str(activity.get("id")),
        "name": f.formate_str(activity.get("name", "")),
        "start_date": f.formate_str(activity.get("start_date", "").split("T")[0]),
        "sport_type": f.formate_str(activity.get("type", "")),
        "duree": f.get_value(activity, "moving_time", "num"),
        "distance": f.get_value(activity, "distance", "num"),
        "materiel": f.get_gear(activity.get("gear_id", "")),
    }


def update_database():
    """Met à jour la base de données avec les nouvelles activités."""
    disable_ssl_warnings()

    print("Authentification...")
    access_token = get_access_token(p.auth_url, p.payload)
    print(f"Jeton d'accès obtenu : {access_token}\n")

    headers = {"Authorization": f"Bearer {access_token}"}
    page_number = 1
    new_activities = 0
    consecutive_known = 0

    while True:
        activities = fetch_activities_page(p.activity_url, headers, page_number)
        if not activities:
            break

        for index, activity in enumerate(activities):
            print(f"\rTraitement activité {index + 1} : {activity.get('name')}", end="")

            activity_id = activity.get("id")
            if f.is_unknown_activity(activity_id):
                formatted = process_activity(activity)
                if formatted["materiel"] is None:
                    gear_id = activity.get("gear_id", "")
                    formatted["materiel"] = f.add_gear(headers, gear_id)
                f.add_activity(formatted)
                new_activities += 1
                consecutive_known = 0
            else:
                consecutive_known += 1
                if consecutive_known > 5:
                    print("\nTrop d'activités connues d'affilée, arrêt anticipé.")
                    p.db_connector.commit()
                    print(f"\n{new_activities} nouvelles activités ajoutées.")
                    return new_activities

        page_number += 1

    p.db_connector.commit()
    print(f"\n{new_activities} nouvelles activités ajoutées.")
    return new_activities
