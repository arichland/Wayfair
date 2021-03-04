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
            order_type TEXT,
            po_date DATE,
            po_number TEXT,
            price DOUBLE,
            quantity INT,
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
            Voucher_ID INT)
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

        
def create_tables():
    create_tbl_wf_orders()
    create_tbl_wf_inventory()
    create_tbl_wf_vouchers()
create_tables()