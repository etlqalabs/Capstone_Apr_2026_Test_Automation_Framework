import pandas as pd
import cx_Oracle
import pytest
from sqlalchemy import create_engine
import logging

from commonUtilities.utilities import ValidationUtility, BaseUtility
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

@pytest.mark.usefixtures("connect_to_oracle_database","connect_to_mysql_database")
class TestDataExtraction:
    validation_utility = ValidationUtility()
    base_utility = BaseUtility()

    @pytest.mark.skip
    def test_data_extraction_from_sales_file_to_stag(self,connect_to_mysql_database):
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            query_actual = """select * from stag_sales"""
            self.validation_utility.execute_validation(
                validation_type="S3_TO_DB",
                test_case_name = test_case_name,
                bucket_name=BUCKET_NAME,
                file_key=FILE_KEY,
                query_actual = query_actual,
                db_actual= connect_to_mysql_database
            )
        except Exception as e:
            self.base_utility.log_error(f"{test_case_name} validation failed: {e}")
            pytest.fail()

    def test_data_extraction_from_products_file_to_stag(self,connect_to_mysql_database):
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            self.base_utility.log_info(f"===== Starting test: {test_case_name} =====")
            #self.linux_utility_download_file_from_linux_server()
            self.base_utility.log_info("Step 1: Downloading products file from Linux server.")
            #self.validation_utility.linux_utility_download_file_from_linux_server()
            self.base_utility.log_info("Products file downloaded successfully.")
            query_actual = """select * from stag_products"""
            self.validation_utility.execute_validation(
                validation_type="FILE_TO_DB",
                test_case_name = test_case_name,
                file_path=LOCAL_FILE_PATH,
                file_type="csv",
                query_actual = query_actual,
                db_actual= connect_to_mysql_database
            )
        except Exception as e:
            self.base_utility.log_error(f"{test_case_name} validation failed: {e}")
            pytest.fail()


    @pytest.mark.skip
    def test_data_extraction_from_inventory_file_to_stag(self,connect_to_mysql_database):
        pass


    def test_data_extraction_from_supplier_file_to_stag(self,connect_to_mysql_database):
        test_case_name = inspect.currentframe().f_code.co_name

        try:
            self.base_utility.log_info(f"===== Starting test: {test_case_name} =====")
            self.base_utility.log_info("Step 1: Preparing database query for validation.")
            query_actual = """select * from stag_supplier"""
            self.base_utility.log_info("Step 2: Validating supplier JSON data with staging table.")
            self.validation_utility.execute_validation(
                validation_type="FILE_TO_DB",
                test_case_name=test_case_name,
                file_path="testData/supplier_data.json",
                file_type="json",
                query_actual=query_actual,
                db_actual=connect_to_mysql_database
            )
            self.base_utility.log_info(f"===== Test Passed: {test_case_name} =====")

        except Exception as e:
            self.base_utility.log_error(f"===== Test Failed: {test_case_name} =====")
            self.base_utility.log_error(f"Reason: {e}")
            pytest.fail(str(e))


    @pytest.mark.skip
    def test_data_extraction_from_stores_oracle_to_stag_mysql(self,connect_to_oracle_database,connect_to_mysql_database):
        pass