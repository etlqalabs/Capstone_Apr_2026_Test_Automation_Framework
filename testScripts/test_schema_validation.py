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


    def test_schema_validation_column_name_for_fact_inventory(self,connect_to_mysql_database):
        expected_columns = ['product_id','store_id','quantity_on_hand','last_updated']
        self.schema_validation.validate_column_names(connect_to_mysql_database,"fact_inventory",expected_columns)

    @pytest.mark.skip
    def test_schema_validation_column_name_for_inventory_level_by_stores(self, connect_to_mysql_database):
        pass

    @pytest.mark.skip
    def test_schema_validation_column_name_for_monthly_sales_summary(self, connect_to_mysql_database):
        pass



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