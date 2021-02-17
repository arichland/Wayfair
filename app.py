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

def sql_wf_po():
    print("   PO Data to SQL: Start")
    con = pymysql.connect(user=user,
                          password=password,
                          host=host,
                          database=db,
                          charset=charset,
                          cursorclass=cusrorType)

    for i in orders.values():
        po_number = i['po_number']
        cust_address1 = i['cust_address1']
        cust_address2 = i['cust_address2']
        cust_city = i['cust_city']
        cust_name = i['cust_name']
        cust_post_code = i['cust_post_code']
        cust_state = i['cust_state']
        est_ship_date = i['est_ship_date']
        order_type = i['order_type']
        po_date = i['po_date']
        price = i['price']
        quantity = i['quantity']
        ship_address1 = i['ship_address1']
        ship_address2 = i['ship_address2']
        ship_address3 = i['ship_address3']
        ship_city = i['ship_city']
        ship_country = i['ship_country']
        ship_name = i['ship_name']
        ship_phone = i['ship_phone']
        ship_post_code = i['ship_post_code']
        ship_state = i['ship_state']
        sku = i['sku']

        qry_insert_orders = """Insert into Wayfair.tbl_WF_POs(
        import_timestamp,
        cust_address1,
        cust_address2,
        cust_city,
        cust_name,
        cust_post_code,
        cust_state,
        est_ship_date,
        order_type,
        po_date,
        po_number,
        price,
        quantity,
        ship_address1,
        ship_address2,
        ship_address3,
        ship_city,
        ship_country,
        ship_name,
        ship_phone,
        ship_post_code,
        ship_state,
        sku) 
        Values(Now(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        with con.cursor() as cur:
            cur.execute(qry_insert_orders, (cust_address1,
                                              cust_address2,
                                              cust_city,
                                              cust_name,
                                              cust_post_code,
                                              cust_state,
                                              est_ship_date,
                                              order_type,
                                              po_date,
                                              po_number,
                                              price,
                                              quantity,
                                              ship_address1,
                                              ship_address2,
                                              ship_address3,
                                              ship_city,
                                              ship_country,
                                              ship_name,
                                              ship_phone,
                                              ship_post_code,
                                              ship_state,
                                              sku))
        con.commit()

def api_wf_orders():
    print("Start of Wayfair Purchase Order Data Collection")
    print("     PO API Call: Start")
    vars = '''null'''
    call_orders = call('orders') %(td)
    token = fetch_token(client_id, client_secret)
    response = prep_request(token, call_orders, vars)
    data = response['data']['getDropshipPurchaseOrders']
    pp.pprint(data)
    count = 0
    for i in data:
        po_number = i['poNumber']
        cust_address1 = i['customerAddress1']
        cust_address2 = i['customerAddress2']
        cust_city = i['customerCity']
        cust_name = i['customerName']
        cust_post_code = i['customerPostalCode']
        cust_state = i['customerState']
        est_ship_date = i['estimatedShipDate']
        order_type = i['orderType']
        po_date = i['poDate']
        ship_to = i['shipTo']
        ship_address1 = ship_to.get('address1')
        ship_address2 = ship_to.get('address2')
        ship_address3 = ship_to.get('address3')
        ship_city = ship_to.get('city')
        ship_country = ship_to.get('country')
        ship_name = ship_to.get('name')
        ship_phone = ship_to.get('phoneNumber')
        ship_post_code = ship_to.get('postalCod')
        ship_state = ship_to.get('state')
        products = i['products']

        for i in products:
            count += 1
            sku = i['partNumber']
            price = i['price']
            quantity = int(i['quantity'])
            temp = {count: {
                'cust_address1': cust_address1,
                'cust_address2': cust_address2,
                'cust_city': cust_city,
                'cust_post_code': cust_post_code,
                'cust_name': cust_name,
                'cust_state': cust_state,
                'est_ship_date': est_ship_date,
                'order_type': order_type,
                'po_date': po_date,
                'po_number': po_number,
                'price': price,
                'quantity': quantity,
                'ship_address1': ship_address1,
                'ship_address2': ship_address2,
                'ship_address3': ship_address3,
                'ship_city': ship_city,
                'ship_country': ship_country,
                'ship_name': ship_name,
                'ship_phone': ship_phone,
                'ship_post_code': ship_post_code,
                'ship_state': ship_state,
                'sku': sku
            }}
            orders.update(temp)

    print("     PO API Call: Complete")
    sql_wf_po()
    print("Completed Wayfair Purchase Order Data Collection")
api_wf_orders()

