import json
import requests

from azure.keyvault import KeyVaultClient, KeyVaultAuthentication
from azure.common.credentials import ServicePrincipalCredentials


def auth_callback(server, resource, scope):
    params = {'api-version':'2018-02-01', 'resource':resource}
    headers = {'Metadata':'true'}
    token = requests.get('http://169.254.169.254/metadata/identity/oauth2/token',params=params, headers=headers).json()
    
    return token['token_type'], token['access_token']

    
def get_app_secret(vault_url, secret_name, secret_version=''):
    """ Return (client_id, client_secret).
    """
    client = KeyVaultClient(KeyVaultAuthentication(auth_callback))
    resp = client.get_secret(vault_url, secret_name, secret_version)
    secret = json.loads(resp.value)
    
    return secret['client_id'], secret['client_secret']
