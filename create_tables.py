_author_ = 'arichland'
import pymysql
import pydict

# SQL DB Connection Fields
sql = pydict.sql_dict.get
user = sql('user')
password = sql('password')
host = sql('host')
db = sql('database')
charset = sql('charset')
cusrorType = pymysql.cursors.DictCursor

def create_tbl_wf_orders():
    con = pymysql.connect(user=user, password=password, host=host, database=db, charset=charset, cursorclass=cusrorType)
    with con.cursor() as cur:
        qry_create_table = """CREATE TABLE IF NOT EXISTS tbl_wf_orders(
            id INT AUTO_INCREMENT PRIMARY KEY,
            import_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            cust_address1 TEXT,
            cust_address2 TEXT,
            cust_city TEXT,
            cust_name TEXT,
            cust_post_code TEXT,
            cust_state TEXT,
            est_ship_date DATE,
            month INT,
            order_type TEXT,
            po_date DATE,
            po_number TEXT,
            price DOUBLE,
            quantity INT,
            quarter INT,
            ship_address1 TEXT,
            ship_address2 TEXT,
            ship_address3 TEXT,
            ship_city TEXT,
            ship_country TEXT,
            ship_name TEXT,
            ship_phone TEXT,
            ship_post_code TEXT,
            ship_state TEXT,
            sku TEXT,
            voucher_id INT,
            year INT)
            ENGINE=INNODB;"""
        cur.execute(qry_create_table)
    con.commit()
    cur.close()
    con.close()

def create_tbl_wf_inventory():
    con = pymysql.connect(user=user, password=password, host=host, database=db, charset=charset, cursorclass=cusrorType)
    with con.cursor() as cur:
        qry_create_table = """
        CREATE TABLE IF NOT EXISTS tbl_wf_inventory(
        id INT AUTO_INCREMENT PRIMARY KEY,
        discontinued TEXT,
        quantityBackordered INT,
        quantityOnHand INT,
        quantityOnOrder INT,
        sku TEXT)
        ENGINE=INNODB;"""
        cur.execute(qry_create_table)
    con.commit()
    cur.close()
    con.close()

def create_tbl_wf_vouchers():
    con = pymysql.connect(user=user, password=password, host=host, database=db, charset=charset, cursorclass=cusrorType)
    with con.cursor() as cur:
        qry_create_table = """CREATE TABLE IF NOT EXISTS tbl_wf_vouchers(
        id INT AUTO_INCREMENT PRIMARY KEY,
        voucher_id BIGINT,
        voucher_date DATE,
        status TEXT,
        status_date DATE,
        amount DOUBLE)
        ENGINE=INNODB;"""
        cur.execute(qry_create_table)
    con.commit()
    cur.close()
    con.close()

def create_tbl_wf_catelog():
    con = pymysql.connect(user=user, password=password, host=host, database=db, charset=charset, cursorclass=cusrorType)
    with con.cursor() as cur:
        qry_create_table = """CREATE TABLE IF NOT EXISTS tbl_wf_catelog(
        id INT AUTO_INCREMENT PRIMARY KEY,
        canada_code INT,
        collection_name TEXT,
        display_set_quantity INT,
        force_multiples VARCHAR(5),
        full_retail_price INT,
        harmonized_code INT,
        lead_time INT,
        lead_time_for_replacement_parts INT,
        manufacturer_country TEXT,
        manufacturer_name TEXT,
        map_price INT,
        min_order_quantity INT,
        product_name TEXT,
        sku TEXT,
        sku_status TEXT,
        sku_substatus TEXT,
        supplier_id INT,
        supplier_part_number TEXT,
        upc BIGINT,
        wayfair_class TEXT,
        wayfair_sku TEXT,
        white_labeled VARCHAR(5),
        wholesale_price INT)
        ENGINE=INNODB;"""
        cur.execute(qry_create_table)
    con.commit()
    cur.close()
    con.close()

def create_tables():
    create_tbl_wf_orders()
    create_tbl_wf_inventory()
    create_tbl_wf_vouchers()
    create_tbl_wf_catelog()
create_tables()