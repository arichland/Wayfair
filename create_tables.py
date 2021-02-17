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

# Establish connection to SQL DB
con = pymysql.connect(user=user,
                      password=password,
                      host=host,
                      database=db,
                      charset=charset,
                      cursorclass=cusrorType)

def create_tbl_wf_po():
    with con.cursor() as cur:
        qry_create_table = """CREATE TABLE IF NOT EXISTS tbl_WF_POs(
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

def create_tbl_api_log():
    with con.cursor() as cur:
        qry_create_table = """CREATE TABLE IF NOT EXISTS tbl_API_Log(
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME,
        api TEXT,
        data TEXT,
        api_code TEXT,
        code_descr TEXT)
        ENGINE=INNODB;"""
        cur.execute(qry_create_table)
    con.commit()
    con.close()

def create_tables():
    create_tbl_wf_po()
    #create_tbl_api_log()
create_tables()