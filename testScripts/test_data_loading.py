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
class TestDataLoading:
    validation_utility = ValidationUtility()
    base_utility = BaseUtility()

    @pytest.mark.regression
    def test_data_loading_for_monthly_sales_summary(self,connect_to_mysql_database):
        test_case_name = inspect.currentframe().f_code.co_name

        try:
            self.base_utility.log_info(f"===== Starting test: {test_case_name} =====")
            self.base_utility.log_info("Step 1: Preparing database query for validation.")
            query_expected = """select ms.product_id,ms.month,ms.year,ms.total_sales 
                                from monthly_sales_summary_source as ms order by ms.product_id"""
            query_actual = """select m.product_id,m.month,m.year,m.total_sales 
                                from monthly_sales_summary as m order by m.product_id"""
            self.base_utility.log_info("Step 2: Validating data loading for monthly sales summary")
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

    @pytest.mark.regression
    @pytest.mark.regression
    def test_data_loading_for_fact_sales(self,connect_to_mysql_database):
        test_case_name = inspect.currentframe().f_code.co_name

        try:
            self.base_utility.log_info(f"===== Starting test: {test_case_name} =====")
            self.base_utility.log_info("Step 1: Preparing database query for validation.")
            query_expected = """select sd.sales_id,sd.product_id,sd.store_id,sd.quantity,sd.sales_amount as total_sales,
                                sd.sale_date from sales_with_details as sd order by sd.sales_id,sd.product_id,sd.store_id"""
            query_actual = """select fs.sales_id,fs.product_id,fs.store_id,fs.quantity,round(fs.total_sales,0) as total_sales,fs.sale_date 
                              from fact_sales as fs order by fs.sales_id,fs.product_id,fs.store_id"""
            self.base_utility.log_info("Step 2: Validating data loading for fact_sales")
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

    @pytest.mark.skip
    def test_data_loading_for_fact_inventory(self, connect_to_mysql_database):
        pass

    @pytest.mark.skip
    def test_data_loading_for_inventory_levl_by_stores(self, connect_to_mysql_database):
        pass