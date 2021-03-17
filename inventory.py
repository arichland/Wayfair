_author_ = 'arichland'

import pydict
import pprint
import pymysql
import api
pp = pprint.PrettyPrinter(indent=1)

inven_query = """mutation save (
            $inventory: [inventoryInput]!,
            $feedKind: inventoryFeedKind) 
            {inventory 
            {save (inventory: $inventory,
            feedKind: $feedKind) 
            {id,handle,status,submittedAt,completedAt,errors {key,message}}}}"""

inven_vars = """{"inventory":
                 [{"supplierId": 56992,
                   "supplierPartNumber": "A11101",
                   "quantityOnHand": 50
                   "quantityBackordered": 0,
                   "quantityOnOrder": 0,
                   "itemNextAvailabilityDate": "",
                   "productNameAndOptions": "",
                   "discontinued": False}],
                   "feedKind": "TRUEUP"}"""

def wf_inventory():
    print("Start of Wayfair Catelog API Call")

    # API Fields
    call = pydict.wf_api_calls.get
    auth = pydict.api_auth
    client_id = auth['client_id']
    client_secret = auth['client_secret']

    vars = inven_vars
    #url = call('inventory') % (limit)
    url = inven_query
    token = api.fetch_token(client_id, client_secret)
    response = api.prep_request(token, url, vars)
    data = response['data']['inventory']
    for i in data:
        pp.pprint(i)
        discontinued = i['discontinued']
        quantityBackordered = i['quantityBackordered']
        quantityOnHand = i['quantityOnHand']
        quantityOnOrder = i['quantityOnOrder']
        sku = i['supplierPartNumber']
wf_inventory()