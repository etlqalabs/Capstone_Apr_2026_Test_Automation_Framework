import pandas as pd
import cx_Oracle
import pytest
from sqlalchemy import create_engine
import logging

from commonUtilities.utilities import ValidationUtility
from testConfiguration.etl_config import *
import inspect


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
    validation_utility = ValidationUtility()

    @pytest.mark.skip
    def test_data_extraction_from_sales_file_to_stag(self):
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            query_actual = """select * from stag_sales"""
            self.validation_utility.execute_validation(
                validation_type="S3_TO_DB",
                test_case_name = test_case_name,
                bucket_name=BUCKET_NAME,
                file_key=FILE_KEY,
                query_actual = query_actual,
                db_actual= mysql_conn
            )
        except Exception as e:
            logger.error(f"Sales data extraction validation failed {e}")

    def test_data_extraction_from_products_file_to_stag(self):
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            self.linux_utility_download_file_from_linux_server()
            query_actual = """select * from stag_products"""
            self.validation_utility.execute_validation(
                validation_type="FILE_TO_DB",
                test_case_name = test_case_name,
                file_path=LOCAL_FILE_PATH,
                file_type="csv",
                query_actual = query_actual,
                db_actual= mysql_conn
            )
        except Exception as e:
            logger.error(f"product data extraction validation failed {e}")

    @pytest.mark.skip
    def test_data_extraction_from_inventory_file_to_stag(self):
        pass

    @pytest.mark.skip
    def test_data_extraction_from_supplier_file_to_stag(self):
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            query_actual = """select * from stag_supplier"""
            self.validation_utility.execute_validation(
                validation_type="FILE_TO_DB",
                test_case_name = test_case_name,
                file_path="testData/supplier_data.json",
                file_type="json",
                query_actual = query_actual,
                db_actual= mysql_conn
            )
        except Exception as e:
            logger.error(f"product data extraction validation failed {e}")

    @pytest.mark.skip
    def test_data_extraction_from_stores_oracle_to_stag_mysql(self):
        pass