import os
from grafana_api.grafana_face import GrafanaFace

def grafana_query(email):
    grafana_api = GrafanaFace(
        auth=(os.getenv('GRAFANA_USER'), os.getenv('GRAFANA_PASSWORD')),
        host=os.getenv('GRAFANA_HOST')
    )
    try:
        user = grafana_api.users.find_user(email)
        if user:
            return {"response": {"user": user}}
        else:
            return {"response": "No user found."}
    except Exception as e:
        return {"response": {"error": str(e)}}

