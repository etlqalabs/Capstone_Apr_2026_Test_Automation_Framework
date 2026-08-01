import pandas as pd
import cx_Oracle
import pytest
from sqlalchemy import create_engine
import logging

from commonUtilities.utilities import ValidationUtility, BaseUtility, SchemaValidation
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
class TestSchemaValidation:
    schema_validation = SchemaValidation()

    @pytest.mark.skip
    def test_schema_validation_column_name_for_fact_sales(self,connect_to_mysql_database):
        expected_columns = [
                            'sales_id',
                            'product_id',
                            'store_id',
                            'quantity',
                            'total_sales',
                            'sale_date'
                            ]

        self.schema_validation.validate_column_names(connect_to_mysql_database,"fact_sales",expected_columns)

    @pytest.mark.skip
    def test_schema_validation_column_name_for_fact_inventory(self,connect_to_mysql_database):
        expected_columns = ['product_id','store_id','quantity_on_hand','last_updated']
        self.schema_validation.validate_column_names(connect_to_mysql_database,"fact_inventory",expected_columns)

    @pytest.mark.skip
    def test_schema_validation_column_name_for_inventory_level_by_stores(self, connect_to_mysql_database):
        pass

    @pytest.mark.skip
    def test_schema_validation_column_name_for_monthly_sales_summary(self, connect_to_mysql_database):
        pass

    @pytest.mark.skip
    def test_schema_validation_data_types_for_fact_inventory(self, connect_to_mysql_database):

        expected_datatypes = {
                'product_id': ["int64"],
                'store_id': ["int64"],
                'quantity_on_hand': ["int64"],
                'last_updated':["object"]
        }

        self.schema_validation.validate_columns_dataTypes(connect_to_mysql_database,"fact_inventory",expected_datatypes)



    @pytest.mark.skip
    def test_schema_validation_data_types_for_fact_sales(self, connect_to_mysql_database):
        pass

    @pytest.mark.skip
    def test_schema_validation_data_types_for_inventory_level_by_stores(self, connect_to_mysql_database):
        pass

    @pytest.mark.skip
    def test_schema_validation_data_types_for_monthly_sales_summary(self, connect_to_mysql_database):
        pass

    def test_schema_validation_referential_integrity_check_for_product_id_in_child_table_fact_sales_and_parent_table_stag_products(self,connect_to_mysql_database):
        try:
            foreign_query = """select * from fact_sales"""
            primary_query = """select * from stag_products"""
            df_not_matched = self.schema_validation.checkReferentialIntegrity(
            source_db_conn = connect_to_mysql_database,
            target_db_conn = connect_to_mysql_database,
            foreign_query = foreign_query,
            primary_query= primary_query,
            key_column = "product_id",
            csv_path = ("differences/foreign_key_not_matching.csv"))
            assert df_not_matched.empty, "There are some additional rows in foregin key column"
        except Exception as e:
            logger.error(f"Error while perfroming Referential Integrity chekc {e}")
            pytest.fail(f"Error while perfroming Referential Integrity check")

    @pytest.mark.skip
    def test_schema_validation_referential_integrity_check_for_sales_id_in_child_table_fact_sales_and_parent_table_stag_sales(
            self, connect_to_mysql_database):
        pass

    @pytest.mark.skip
    def test_schema_validation_referential_integrity_check_for_store_id_in_child_table_fact_sales_and_parent_table_stag_stores(
            self, connect_to_mysql_database):
        pass