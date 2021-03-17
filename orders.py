_author_ = 'arichland'

import requests
import pydict
import pprint
import datetime
import pymysql
import api
pp = pprint.PrettyPrinter(indent=1)

def wf_orders(update_date):
    print("Start of Wayfair Purchase Order API Call")

    # API Fields
    call = pydict.wf_api_calls.get
    auth = pydict.api_auth
    client_id = auth['client_id']
    client_secret = auth['client_secret']
    limit = 100
    vars = '''null'''
    url = call('orders') % (limit, update_date)
    token = api.fetch_token(client_id, client_secret)
    response = api.prep_request(token, url, vars)
    data = response['data']['getDropshipPurchaseOrders']
    #pp.pprint(data)
    sql_orders(data)

def sql_orders(data):
    # Database Fields
    sql = pydict.sql_dict.get
    user = sql('user')
    password = sql('password')
    host = sql('host')
    db = sql('database')

    # Date Formatting
    dtime = datetime.datetime
    date = datetime.date
    delta = datetime.timedelta
    strip = dtime.strptime
    strip_format = "%Y-%m-%d %H:%M:%S.%f %z"
    now = dtime.now()
    ts = dtime.fromtimestamp

    print("   PO Data to SQL: Start")

    con = pymysql.connect(user=user, password=password, host=host, database=db)
    with con.cursor() as cur:
        print("     Creating temp table")
        qry_temp_table = """CREATE TEMPORARY TABLE IF NOT EXISTS tbl_temp LIKE wayfair.tbl_wf_orders;"""
        cur.execute(qry_temp_table)

        print("     Inserting API data into temp table")
        for i in data:
            po_date = i['poDate']
            cust_address1 = i['customerAddress1']
            cust_address2 = i['customerAddress2']
            cust_city = i['customerCity']
            cust_name = i['customerName']
            cust_post_code = i['customerPostalCode']
            cust_state = i['customerState']
            est_ship_date = i['estimatedShipDate']
            month = strip(po_date, strip_format).month
            order_type = i['orderType']
            po_number = i['poNumber']
            quarter = ((strip(po_date, strip_format).month - 1) // 3) + 1
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
            year = strip(po_date, strip_format).year

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
                        month,
                        order_type,
                        po_date,
                        po_number,
                        price,
                        quantity,
                        quarter,
                        ship_address1,
                        ship_address2,
                        ship_address3,
                        ship_city,
                        ship_country,
                        ship_name,
                        ship_phone,
                        ship_post_code,
                        ship_state,
                        sku,
                        year) 
                        Values(Now(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
                cur.execute(qry_temp_data, (cust_address1,
                                            cust_address2,
                                            cust_city,
                                            cust_name,
                                            cust_post_code,
                                            cust_state,
                                            est_ship_date,
                                            month,
                                            order_type,
                                            po_date,
                                            po_number,
                                            price,
                                            quantity,
                                            quarter,
                                            ship_address1,
                                            ship_address2,
                                            ship_address3,
                                            ship_city,
                                            ship_country,
                                            ship_name,
                                            ship_phone,
                                            ship_post_code,
                                            ship_state,
                                            sku,
                                            year))
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
                        month,
                        order_type,
                        po_date,
                        po_number,
                        price,
                        quantity,
                        quarter,
                        ship_address1,
                        ship_address2,
                        ship_address3,
                        ship_city,
                        ship_country,
                        ship_name,
                        ship_phone,
                        ship_post_code,
                        ship_state,
                        sku,
                        year)

                    SELECT
                        SQ1.import_timestamp,
                        SQ1.cust_address1,
                        SQ1.cust_address2,
                        SQ1.cust_city,
                        SQ1.cust_name,
                        SQ1.cust_post_code,
                        SQ1.cust_state,
                        SQ1.est_ship_date,
                        SQ1.month,
                        SQ1.order_type,
                        SQ1.po_date,
                        SQ1.po_number,
                        SQ1.price,
                        SQ1.quantity,
                        SQ1.quarter,
                        SQ1.ship_address1,
                        SQ1.ship_address2,
                        SQ1.ship_address3,
                        SQ1.ship_city,
                        SQ1.ship_country,
                        SQ1.ship_name,
                        SQ1.ship_phone,
                        SQ1.ship_post_code,
                        SQ1.ship_state,
                        SQ1.sku,
                        SQ1.year
                    FROM(SELECT
                        import_timestamp,
                        cust_address1,
                        cust_address2,
                        cust_city,
                        cust_name,
                        cust_post_code,
                        cust_state,
                        est_ship_date,
                        month,
                        order_type,
                        po_date,
                        po_number,
                        price,
                        quantity,
                        quarter,
                        ship_address1,
                        ship_address2,
                        ship_address3,
                        ship_city,
                        ship_country,
                        ship_name,
                        ship_phone,
                        ship_post_code,
                        ship_state,
                        sku,
                        year
                        FROM tbl_temp) AS SQ1 LEFT JOIN tbl_wf_orders ON SQ1.po_number = tbl_wf_orders.po_number WHERE tbl_wf_orders.po_number IS NULL;"""
        cur.execute(qry_insert_new_data)
        con.commit()
    cur.close()
    con.close()
    print("Process Complete")