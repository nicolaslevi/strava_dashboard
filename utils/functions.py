import utils.params as p
import requests
import urllib3
import time


def is_unknown_activity(activity_id):
    activity = """ SELECT id FROM activities_infos WHERE id={}; """.format(activity_id)
    res = p.db_cursor.execute(activity).fetchall()
    return len(res) == 0


def is_unknown_segment(segment_id):
    """
    Vérifie si l'id du segment est présent dans la BDD
    :param segment_id:
    :param cursor:
    :return: True si le segment n'est pas dans la BDD
    """
    rode_segment = """ SELECT id FROM segments_infos WHERE id={}; """.format(segment_id)
    res = p.db_cursor.execute(rode_segment).fetchall()
    return len(res) == 0


def formate_str(string):
    if string is None:
        string = "N.A"
    string = str(string).replace("'", "''")
    return "'{}'".format(string.replace("'", "''"))


def get_value(json, cle, typ):
    if typ == "str":
        val = str(json.get(cle) or "N.A")
        val = "'{}'".format(val.replace("'", "''"))

    elif typ == "num":
        val = str(json.get(cle) or "null")

    elif typ == "speed":
        long = json.get(cle[0])
        time = json.get(cle[1])

        if time == 0:
            val = "null"
        else:
            val = str(round(long / time * 3.6, 1))

    else:
        val = "null"

    return val


def create_segment(segment_infos):
    requete = """INSERT INTO segments_infos (%s )
                     VALUES (%s);""" % (
        ", ".join(list(segment_infos.keys())),
        ", ".join(list(segment_infos.values())),
    )
    p.db_cursor.execute(requete)


def add_perf(perf_infos):
    requete = """INSERT INTO segments_performances (%s )
                     VALUES (%s);""" % (
        ", ".join(list(perf_infos.keys())),
        ", ".join(list(perf_infos.values())),
    )
    p.db_cursor.execute(requete)


def add_activity(activity_infos):
    requete = """INSERT INTO activities_infos (%s )
                     VALUES (%s);""" % (
        ", ".join(list(activity_infos.keys())),
        ", ".join(list(activity_infos.values())),
    )
    p.db_cursor.execute(requete)


def request(url, headers, params={}):
    res = requests.get(url, headers=headers, params=params).json()
    while type(res) == dict and res.get("message") == "Rate Limit Exceeded":
        print("Rate Limit Exceeded, waiting 10min")
        time.sleep(900)
        print("Script resume")
        res = requests.get(url, headers=headers, params=params).json()

    return res


def retrieve_workout(conds=dict()):
    if len(conds) == 0:
        requete = """SELECT * FROM  activities_infos;"""
    else:
        requete = """SELECT * FROM  activities_infos WHERE %s;""" % (
            " AND ".join([k + '"' + v + '"' for k, v in conds.items()])
        )
    return p.db_cursor.execute(requete).fetchall()


def retrieve_col_name(table):
    req = """SELECT name FROM PRAGMA_TABLE_INFO('{}');""".format(table)
    return p.db_cursor.execute(req).fetchall()
