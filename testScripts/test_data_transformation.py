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


@pytest.mark.usefixtures("connect_to_mysql_database")
class TestDataTransformation:
    validation_utility = ValidationUtility()
    base_utility = BaseUtility()


    def test_data_transformation_for_filter_sales_data(self,connect_to_mysql_database):
        test_case_name = inspect.currentframe().f_code.co_name

        try:
            self.base_utility.log_info(f"===== Starting test: {test_case_name} =====")
            self.base_utility.log_info("Step 1: Preparing database query for validation.")
            query_expected = """select sales_id,product_id,store_id,quantity,price,sale_date,
                                region from stag_sales where sale_date>='2024-09-10'"""
            query_actual = """select sales_id,product_id,store_id,quantity,price,sale_date,region 
                                from filtered_sales"""
            self.base_utility.log_info("Step 2: Validating filter transformation.")
            self.validation_utility.execute_validation(
                validation_type="DB_TO_DB",
                test_case_name=test_case_name,
                query_expected=query_expected,
                db_expected=connect_to_mysql_database,
                query_actual=query_actual,
                db_actual=connect_to_mysql_database
            )
            self.base_utility.log_info(f"===== Test Passed: {test_case_name} =====")

        except Exception as e:
            self.base_utility.log_error(f"===== Test Failed: {test_case_name} =====")
            self.base_utility.log_error(f"Reason: {e}")
            pytest.fail(str(e))


    def test_data_transformation_for_router_high_sales_data(self,connect_to_mysql_database):
        test_case_name = inspect.currentframe().f_code.co_name

        try:
            self.base_utility.log_info(f"===== Starting test: {test_case_name} =====")
            self.base_utility.log_info("Step 1: Preparing database query for validation.")
            query_expected = """select sales_id,product_id,store_id,quantity,price,sale_date,region 
                                from filtered_sales where region='High'"""
            query_actual = """select sales_id,product_id,store_id,quantity,price,sale_date,region from high_sales"""
            self.base_utility.log_info("Step 2: Validating Router - High transformation.")
            self.validation_utility.execute_validation(
                validation_type="DB_TO_DB",
                test_case_name=test_case_name,
                query_expected=query_expected,
                db_expected=connect_to_mysql_database,
                query_actual=query_actual,
                db_actual=connect_to_mysql_database
            )
            self.base_utility.log_info(f"===== Test Passed: {test_case_name} =====")

        except Exception as e:
            self.base_utility.log_error(f"===== Test Failed: {test_case_name} =====")
            self.base_utility.log_error(f"Reason: {e}")
            pytest.fail(str(e))

    def test_data_transformation_for_router_low_sales_data(self,connect_to_mysql_database):
        test_case_name = inspect.currentframe().f_code.co_name

        try:
            self.base_utility.log_info(f"===== Starting test: {test_case_name} =====")
            self.base_utility.log_info("Step 1: Preparing database query for validation.")
            query_expected = """select sales_id,product_id,store_id,quantity,price,sale_date,region 
                                from filtered_sales where region='Low'"""
            query_actual = """select sales_id,product_id,store_id,quantity,price,sale_date,region from low_sales"""
            self.base_utility.log_info("Step 2: Validating Router -Low transformation.")
            self.validation_utility.execute_validation(
                validation_type="DB_TO_DB",
                test_case_name=test_case_name,
                query_expected=query_expected,
                db_expected=connect_to_mysql_database,
                query_actual=query_actual,
                db_actual=connect_to_mysql_database
            )
            self.base_utility.log_info(f"===== Test Passed: {test_case_name} =====")

        except Exception as e:
            self.base_utility.log_error(f"===== Test Failed: {test_case_name} =====")
            self.base_utility.log_error(f"Reason: {e}")
            pytest.fail(str(e))

    # Please implement below test cases
    @pytest.mark.skip
    def test_data_transformation_for_aggregator_sales(self,connect_to_mysql_database):
        pass

    @pytest.mark.skip
    def test_data_transformation_for_joiner(self,connect_to_mysql_database):
        pass

    @pytest.mark.skip
    def test_data_transformation_for_aggregator_inventory(self,connect_to_mysql_database):
        pass