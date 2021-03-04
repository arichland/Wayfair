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




def wf_inventory():
    print("Start of Wayfair Inventory API Call")
    limit = 100
    vars = '''null'''
    fetch = call('inventory') % (limit)
    token = fetch_token(client_id, client_secret)
    response = prep_request(token, fetch, vars)
    data = response['data']['inventory']
    for i in data:
        pp.pprint(i)
        discontinued = i['discontinued']
        quantityBackordered = i['quantityBackordered']
        quantityOnHand = i['quantityOnHand']
        quantityOnOrder = i['quantityOnOrder']
        sku = i['supplierPartNumber']






wf_inventory()



def wf_orders():
    print("Start of Wayfair Purchase Order API Call")
    limit = 100
    vars = '''null'''
    call_orders = call('orders') % (limit, update_date)
    token = fetch_token(client_id, client_secret)
    response = prep_request(token, call_orders, vars)
    data = response['data']['getDropshipPurchaseOrders']

    print("   PO Data to SQL: Start")
    con = pymysql.connect(user=user, password=password, host=host, database=db, charset=charset, cursorclass=cusrorType)
    with con.cursor() as cur:
        print("     Creating temp table")
        qry_temp_table = """CREATE TEMPORARY TABLE IF NOT EXISTS tbl_temp LIKE wayfair.tbl_wf_orders;"""
        cur.execute(qry_temp_table)

        print("     Inserting API data into temp table")
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
                sku = i['partNumber']
                price = i['price']
                quantity = int(i['quantity'])

                qry_temp_data = """Insert into wayfair.tbl_temp(
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
                cur.execute(qry_temp_data, (cust_address1,
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
        print("   Insert new data into SQL")
        qry_insert_new_data = """
                INSERT INTO tbl_wf_orders(
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
                
                SELECT
                    SQ1.import_timestamp,
                    SQ1.cust_address1,
                    SQ1.cust_address2,
                    SQ1.cust_city,
                    SQ1.cust_name,
                    SQ1.cust_post_code,
                    SQ1.cust_state,
                    SQ1.est_ship_date,
                    SQ1.order_type,
                    SQ1.po_date,
                    SQ1.po_number,
                    SQ1.price,
                    SQ1.quantity,
                    SQ1.ship_address1,
                    SQ1.ship_address2,
                    SQ1.ship_address3,
                    SQ1.ship_city,
                    SQ1.ship_country,
                    SQ1.ship_name,
                    SQ1.ship_phone,
                    SQ1.ship_post_code,
                    SQ1.ship_state,
                    SQ1.sku
                FROM(SELECT
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
                    sku
                    FROM tbl_temp) AS SQ1 LEFT JOIN tbl_wf_orders ON SQ1.po_number = tbl_wf_orders.po_number WHERE tbl_wf_orders.po_number IS NULL;"""
        cur.execute(qry_insert_new_data)
        con.commit()
    cur.close()
    con.close()
    print("Process Complete")
#wf_orders()
