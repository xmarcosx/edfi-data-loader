import base64
import json
import os

import requests
from flask import Flask, request, jsonify
from google.cloud import storage


BASE_URL = os.environ.get('BASE_URL')
API_KEY = os.environ.get('API_KEY')
API_SECRET = os.environ.get('API_SECRET')

# pylint: disable=C0103
app = Flask(__name__)

def get_access_token():
    credentials_concatenated = ':'.join((API_KEY, API_SECRET))
    credentials_encoded = base64.b64encode(credentials_concatenated.encode('utf-8'))
    access_url = f'{BASE_URL}/oauth/token'

    access_headers = {
        'Authorization': b'Basic ' + credentials_encoded
    }

    access_params = {
        'grant_type': 'client_credentials'
    }

    response = requests.post(access_url, headers=access_headers, data=access_params)

    if response.ok:
        response_json = response.json()
        print(response_json['access_token'])
    else:
        raise Exception("Failed to retrieve access token")

def get_file():
    storage_client = storage.Client()

def get_template(template_name: str) -> dict:
    with open('src/nwea.json') as json_file:
        return json.load(json_file)

def post_bootstrap_data(bootstraps, school_year):
    access_token = get_access_token()

    for boostrap in bootstraps:
        payloads = boostrap['Data']
        resource_path = boostrap['ResourcePath']
        endpoint = f'{BASE_URL}/data/v3/{school_year}{resource_path}'
        headers = {"Authorization": f"Bearer {access_token}"}

        for payload in payloads:
            print(payload)
            response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
            response.raise_for_status
            print(response.ok)


@app.route('/')
def main():
    """Return a friendly HTTP greeting."""
    message = "It's running!"

    return message

@app.route('/', methods=['POST'])
def load_data():
    data = request.json
    school_year = data['schoolYear']
    template_name = data['templateName']
    
    template = get_template(template_name)
    
    if data['bootstrap'] == 'TRUE':
        print('Loading bootstrap data')
        post_bootstrap_data(template['Bootstraps'], school_year)
        return 'done'
    else:
        return 'Boostrap is false'


if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
