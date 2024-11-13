# utils/kubernetes.py
import subprocess
import os
import requests

def kubectl(query):
    result = subprocess.getstatusoutput(f"kubectl {query}")    
    return {"response": {"result": result}}

def get_app(app_name='chatbot'):
    return kubectl(f'get applications client-{app_name} -n argocd')

def update_sync_policy(app_name='chatbot', is_sync="true"):
    if is_sync == "true":
        sync_cmd = 'patch --type=merge applications client-' + app_name + ' -p \'{"spec":{"syncPolicy": {"automated": {}}}}\' -n argocd'
        replica_cmd = f'patch --type=merge deployment client-{app_name}-teslamate -p \'{"spec":{"replicas": 1}}\' -n myteslamate'
    else:
        sync_cmd = 'patch --type=merge applications client-'+app_name+' -p \'{"spec":{"syncPolicy": {"automated": null}}}\' -n argocd'
        replica_cmd = f'patch --type=merge deployment client-{app_name}-teslamate -p \'{"spec":{"replicas": 0}}\' -n myteslamate'
    
    kubectl(sync_cmd)
    return kubectl(replica_cmd)

def restore_db(app_name):
    return kubectl(f'exec -it deployment/app -n myteslamate -- php artisan myteslamate:backup:restore --db={app_name}')

def update_grafana(app_name):
    return kubectl(f'exec -it deployment/app -n myteslamate -- php artisan myteslamate:update:all --service={app_name}')


# ArgoCD
def argocd(app_name):
    auth_token = os.getenv('ARGOCD_TOKEN')
    argocd_server = os.getenv('ARGOCD_HOST')
    url = f"{argocd_server}/api/v1/applications/{app_name}"
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return {"response": {"application": response.json()}}
    return {"response": {"error": response.json()}}
