import pandas as pd
import cx_Oracle
from sqlalchemy import create_engine
import logging
from testConfiguration.etl_config import *


# Logger configuration
logging.basicConfig(
    filename = "logs/test_execution.log",
    filemode = 'w',
    format = '%(asctime)s-%(levelname)s-%(message)s',
    level = logging.INFO
   )
logger = logging.getLogger(__name__)

# Database connections

oracle_conn = create_engine(f"oracle+cx_oracle://{ORACLE_USER}:{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}")
mysql_conn = create_engine(F"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}")



class TestDataExtraction:
    def test_data_extraction_from_sales_file_to_stag(self):
        df_expected = pd.read_csv("testData/sales_data_s3.csv")

        df_actual = pd.read_sql("""select * from stag_sales""",mysql_conn)

        assert df_actual.equals(df_expected),"Sales data extraction from file has bene failed"


    def test_data_extraction_from_products_file_to_stag(self):
        df_expected = pd.read_csv("testData/product_data_from_linux_jul18.csv")

        df_actual = pd.read_sql("""select * from stag_products""",mysql_conn)

        assert df_actual.equals(df_expected),"products data extraction from file has bene failed"


    def test_data_extraction_from_inventory_file_to_stag(self):
        pass

    def test_data_extraction_from_supplier_file_to_stag(self):
        pass

    def test_data_extraction_from_stores_oracle_to_stag_mysql(self):
        pass