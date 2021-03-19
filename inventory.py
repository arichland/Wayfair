_author_ = 'arichland'

import pydict
import pprint
import pymysql
import sandbox_api as api
import json
pp = pprint.PrettyPrinter(indent=1)

inven = {
        'A11100': 200,
        'A11101': 6,
        'A11102': 10,
        'A11103': 9,
        'A11104': 10,
        'A11201': 0,
        'A22100': 0,
        'A23101': 0,
        'A23103': 0,
        'A23104': 0,
        'A23201': 0,
        'A23203': 0,
        'A23301': 0,
        'A33100': 0,
        'A35101': 0,
        'A35103': 0,
        'A35201': 0,
        'A35203': 0,
        'A35301': 0,
        'A44100': 0,
        'A46101': 0,
        'A46103': 0,
        'A46201': 0,
        'A46203': 0,
        'A46301': 0,
        'B1101': 10,
        'B1102': 10,
        'B1103': 10,
        'B1104': 10,
        'B1201': 10,
        'B1203': 10,
        'B2101': 0,
        'B2103': 10,
        'B2104': 10,
        'B2202': 10,
        'B2203': 0,
        'B2204': 10,
        'B2301': 10,
        'B3101': 0,
        'B3103': 0,
        'B3202': 9,
        'B3203': 0,
        'B3204': 10,
        'B3301': 10,
        'B4101': 0,
        'B4103': 10,
        'B4202': 10,
        'B4203': 0,
        'B4204': 10,
        'B4301': 10
}

skus = []
def setup():
    # Database Fields
    sql = pydict.sql_dict.get
    user = sql('user')
    password = sql('password')
    host = sql('host')
    db = sql('database')
    con = pymysql.connect(user=user, password=password, host=host, database=db)
    print("   Catelog to SQL: Start")
    inven_dict = """{"inventory":
                      [{"supplierId": 56992,
                        "supplierPartNumber": %s,
                        "quantityOnHand": 0,
                        "quantityBackordered": 0,
                        "quantityOnOrder": 0,
                        "itemNextAvailabilityDate": "",
                        "productNameAndOptions": "",
                        "discontinued": False}],
                  "feedKind": "TRUEUP"}"""

    with con.cursor() as cur:
        print("     Creating temp table")
        qry = """SELECT sku FROM tbl_wf_catelog;"""
        cur.execute(qry)
        rows = cur.fetchall()
        for row in rows:
            inven = inven_dict %(row[0])
            #print(inven)
#setup()

def wf_inventory():
    print("Start of Wayfair Catelog API Call")

    # API Fields
    call = pydict.wf_api_calls.get
    auth = pydict.api_test
    client_id = auth['client_id']
    client_secret = auth['client_secret']
    url = call("inventory_update")
    token = api.fetch_token(client_id, client_secret)
    sku_list =[]
    for k,v in inven.items():
        temp = {"supplierId": 56992,
                "supplierPartNumber": k,
                "quantityOnHand": v,
                "quantityBackordered": 0,
                "quantityOnOrder": 0,
                "itemNextAvailabilityDate": "",
                "productNameAndOptions": "",
                "discontinued": "false"}
        sku_list.append(temp)
    skus = json.dumps(sku_list)
    vars = """{"inventory": %s, "feedKind": "TRUE_UP"}""" %(skus)

    response = api.prep_request(token, url, vars)
    data = response['data']['inventory']
    print(data)

wf_inventory()