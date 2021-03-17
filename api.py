_author_ = 'arichland'

import requests
import pydict
import pprint
import datetime
import pymysql
pp = pprint.PrettyPrinter(indent=1)

# SQL Credentials
sql = pydict.sql_dict.get
call = pydict.wf_api_calls.get
user = sql('user')
password = sql('password')
host = sql('host')
db = sql('database')
charset = sql('charset')
cusrorType = pymysql.cursors.DictCursor

# API Credentials
auth = pydict.api_auth
client_id = auth['client_id']
client_secret = auth['client_secret']
api_url = auth['api_url']
auth_url = auth['auth_url']
dtime = datetime.datetime
date = datetime.date
delta = datetime.timedelta
update_date = date.today() - delta(days=1)
td = date(2020,1,1)

# Dictionaries
orders = {}


def send_request(method: str, url: str, body: str = '', headers: dict = {}):
    response = requests.request(method=method, url=url, data=body, headers=headers)

    if response.status_code == 200:
        return response
    else:
        raise requests.exceptions.RequestException("Request failed: status code {}, response {}".format(response.status_code, response))

def prep_request(token: str, query: str, variables: str):
    headers = {
        'content-type': 'application/json',
        'cache-control': 'no-cache',
        'authorization': 'Bearer {}'.format(token)
    }
    body = '''{"query": "%s","variables": %s}''' % (query, variables)
    try:
        return send_request('POST', api_url, body, headers).json()
    except Exception as err:
        print("Problem executing the GraphQL request: " + str(err))
        exit(1)

def fetch_token(client_id: str, client_secret: str):
    auth_payload = '''
            {
              "grant_type": "client_credentials",
              "client_id": "%s",
              "client_secret": "%s",
              "audience": "https://api.wayfair.com/"
            }
            ''' % (client_id, client_secret)
    headers = {
        'content-type': 'application/json',
        'cache-control': 'no-cache',
    }
    try:
        response = send_request('POST', auth_url, auth_payload, headers).json()
        return response['access_token']
    except Exception as err:
        print("Could not retrieve a token for the request: " + str(err))
        exit(1)


