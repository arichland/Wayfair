_author_ = 'arichland'

import pydict
import pprint
import pymysql
import api
pp = pprint.PrettyPrinter(indent=1)

def sql_catelog(data):
    # Database Fields
    sql = pydict.sql_dict.get
    user = sql('user')
    password = sql('password')
    host = sql('host')
    db = sql('database')

    print("   Catelog to SQL: Start")

    con = pymysql.connect(user=user, password=password, host=host, database=db)
    with con.cursor() as cur:
        print("     Creating temp table")
        qry_temp_table = """CREATE TEMPORARY TABLE IF NOT EXISTS tbl_temp LIKE wayfair.tbl_wf_catelog;"""
        cur.execute(qry_temp_table)

        print("     Inserting categlog data into temp table")
        for i in data:
            canada_code = i['canadaCode']
            collection_name = i['collectionName']
            display_set_quantity = i['displaySetQuantity']
            force_multiples = i['forceMultiples']
            full_retail_price = i['fullRetailPrice']
            harmonized_code = i['harmonizedCode']
            lead_time = i['leadTime']
            lead_time_for_replacement_parts = i['leadTimeForReplacementParts']
            manufacturer_country = i['manufacturerCountry']
            manufacturer_name = i['manufacturerName']
            map_price = i['mapPrice']
            min_order_quantity = i['minimumOrderQuantity']
            product_name = i['productName']
            sku = i['manufacturerModelNumber']
            sku_status = i['skuStatus']
            sku_substatus = i['skuSubstatus']
            supplier_id = i['supplierId']
            supplier_part_number = i['supplierPartNumber']
            upc = i['upc']
            wayfair_class = i['wayfairClass']
            wayfair_sku = i['sku']
            white_labeled = i['whiteLabeled']
            wholesale_price = i['wholesalePrice']

            qry_temp_data = """Insert into wayfair.tbl_temp(
                        canada_code,
                        collection_name,
                        display_set_quantity,
                        force_multiples,
                        full_retail_price,
                        harmonized_code,
                        lead_time,
                        lead_time_for_replacement_parts,
                        manufacturer_country,
                        manufacturer_name,
                        map_price,
                        min_order_quantity,
                        product_name,
                        sku,
                        sku_status,
                        sku_substatus,
                        supplier_id,
                        supplier_part_number,
                        upc,
                        wayfair_class,
                        wayfair_sku,
                        white_labeled,
                        wholesale_price) 
                        Values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            cur.execute(qry_temp_data, (canada_code,
                                        collection_name,
                                        display_set_quantity,
                                        force_multiples,
                                        full_retail_price,
                                        harmonized_code,
                                        lead_time,
                                        lead_time_for_replacement_parts,
                                        manufacturer_country,
                                        manufacturer_name,
                                        map_price,
                                        min_order_quantity,
                                        product_name,
                                        sku,
                                        sku_status,
                                        sku_substatus,
                                        supplier_id,
                                        supplier_part_number,
                                        upc,
                                        wayfair_class,
                                        wayfair_sku,
                                        white_labeled,
                                        wholesale_price))
        print("   Insert new catelog data into SQL")
        qry_insert_new_data = """
                    INSERT INTO tbl_wf_catelog(
                        canada_code,
                        collection_name,
                        display_set_quantity,
                        force_multiples,
                        full_retail_price,
                        harmonized_code,
                        lead_time,
                        lead_time_for_replacement_parts,
                        manufacturer_country,
                        manufacturer_name,
                        map_price,
                        min_order_quantity,
                        product_name,
                        sku,
                        sku_status,
                        sku_substatus,
                        supplier_id,
                        supplier_part_number,
                        upc,
                        wayfair_class,
                        wayfair_sku,
                        white_labeled,
                        wholesale_price)

                    SELECT
                        SQ1.canada_code,
                        SQ1.collection_name,
                        SQ1.display_set_quantity,
                        SQ1.force_multiples,
                        SQ1.full_retail_price,
                        SQ1.harmonized_code,
                        SQ1.lead_time,
                        SQ1.lead_time_for_replacement_parts,
                        SQ1.manufacturer_country,
                        SQ1.manufacturer_name,
                        SQ1.map_price,
                        SQ1.min_order_quantity,
                        SQ1.product_name,
                        SQ1.sku,
                        SQ1.sku_status,
                        SQ1.sku_substatus,
                        SQ1.supplier_id,
                        SQ1.supplier_part_number,
                        SQ1.upc,
                        SQ1.wayfair_class,
                        SQ1.wayfair_sku,
                        SQ1.white_labeled,
                        SQ1.wholesale_price

                    FROM(SELECT
                        canada_code,
                        collection_name,
                        display_set_quantity,
                        force_multiples,
                        full_retail_price,
                        harmonized_code,
                        lead_time,
                        lead_time_for_replacement_parts,
                        manufacturer_country,
                        manufacturer_name,
                        map_price,
                        min_order_quantity,
                        product_name,
                        sku,
                        sku_status,
                        sku_substatus,
                        supplier_id,
                        supplier_part_number,
                        upc,
                        wayfair_class,
                        wayfair_sku,
                        white_labeled,
                        wholesale_price
                        FROM tbl_temp) AS SQ1 LEFT JOIN tbl_wf_catelog ON SQ1.sku = tbl_wf_catelog.sku WHERE tbl_wf_catelog.sku IS NULL;"""
        cur.execute(qry_insert_new_data)
        con.commit()
    cur.close()
    con.close()
    print("Process Complete")

def wf_catelog():
    print("Start of Wayfair Catelog API Call")

    # API Fields
    call = pydict.wf_api_calls.get
    auth = pydict.api_auth
    client_id = auth['client_id']
    client_secret = auth['client_secret']
    limit = 100
    vars = '''null'''
    url = call('catelog') % (limit)
    token = api.fetch_token(client_id, client_secret)
    response = api.prep_request(token, url, vars)
    data = response['data']['productCatalogs']
    sql_catelog(data)

wf_catelog()