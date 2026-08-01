import inspect
import logging
import pytest

from commonUtilities.utilities import (
    ValidationUtility,
    BaseUtility,
    SchemaValidation,
    DataQualityUtility,
    FileUtility
)

from testConfiguration.etl_config import *

logging.basicConfig(
    filename="logs/test_execution.log",
    filemode="w",
    format="%(asctime)s-%(levelname)s-%(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("connect_to_mysql_database")
class TestDataQuality:

    validation_utility = ValidationUtility()
    base_utility = BaseUtility()
    data_quality = DataQualityUtility()
    file_utility = FileUtility()

    # ---------------------------------------------------------------------
    # Duplicate Check
    # ---------------------------------------------------------------------

    def test_data_quality_duplicate_check_for_product_data_csv_file(self):
        test_case_name = inspect.currentframe().f_code.co_name

        try:
            self.base_utility.log_info(f"===== Starting test: {test_case_name} =====")

            duplicate_status = self.data_quality.checkDuplicateInFile(
                "testData/product_data_from_linux.csv",
                "csv"
            )

            logger.info(f"Duplicate Status : {duplicate_status}")

            assert duplicate_status, "There are duplicate records in product_data_from_linux.csv."

            self.base_utility.log_info(f"===== Test Passed: {test_case_name} =====")

        except Exception as e:
            self.base_utility.log_error(f"===== Test Failed: {test_case_name} =====")
            self.base_utility.log_error(f"Reason: {e}")
            pytest.fail(str(e))

    @pytest.mark.skip
    def test_data_quality_duplicate_check_for_sales_data_csv_file(self):
        pass

    @pytest.mark.skip
    def test_data_quality_duplicate_check_for_supplier_data_json_file(self):
        pass

    @pytest.mark.skip
    def test_data_quality_duplicate_check_for_inventory_data_xml_file(self):
        pass

    # ---------------------------------------------------------------------
    # Duplicate Check on Product ID
    # ---------------------------------------------------------------------

    def test_data_quality_duplicate_check_for_product_id_inProduct_data_csv_file(self):
        test_case_name = inspect.currentframe().f_code.co_name

        try:
            self.base_utility.log_info(f"===== Starting test: {test_case_name} =====")

            duplicate_status = self.data_quality.checkDuplicateValuesInFile(
                "testData/product_data_from_linux.csv",
                "csv",
                "product_id"
            )

            logger.info(f"Duplicate Status : {duplicate_status}")

            assert duplicate_status, "There are duplicate product_id values."

            self.base_utility.log_info(f"===== Test Passed: {test_case_name} =====")

        except Exception as e:
            self.base_utility.log_error(f"===== Test Failed: {test_case_name} =====")
            self.base_utility.log_error(f"Reason: {e}")
            pytest.fail(str(e))

    @pytest.mark.skip
    def test_data_quality_duplicate_check_for_sales_id_in_fact_sales_table(self):
        pass

    # ---------------------------------------------------------------------
    # Null Value Check
    # ---------------------------------------------------------------------

    def test_data_quality_null_value_check_for_product_data_csv_file(self):
        test_case_name = inspect.currentframe().f_code.co_name

        try:
            self.base_utility.log_info(f"===== Starting test: {test_case_name} =====")

            null_status = self.data_quality.checkNullValuesInFile(
                "testData/product_data_from_linux.csv",
                "csv"
            )

            logger.info(f"Null Value Status : {null_status}")

            assert null_status, "There are null values in product_data_from_linux.csv."

            self.base_utility.log_info(f"===== Test Passed: {test_case_name} =====")

        except Exception as e:
            self.base_utility.log_error(f"===== Test Failed: {test_case_name} =====")
            self.base_utility.log_error(f"Reason: {e}")
            pytest.fail(str(e))

    # ---------------------------------------------------------------------
    # File Existence Check
    # ---------------------------------------------------------------------

    def test_data_quality_file_existence_check_for_inventory_data_xml_file(self):
        test_case_name = inspect.currentframe().f_code.co_name

        try:
            self.base_utility.log_info(f"===== Starting test: {test_case_name} =====")

            file_exists = self.file_utility.check_file_existence(
                "testData/inventory_data.xml"
            )

            logger.info(f"File Exists : {file_exists}")

            assert file_exists, "inventory_data.xml does not exist."

            self.base_utility.log_info(f"===== Test Passed: {test_case_name} =====")

        except Exception as e:
            self.base_utility.log_error(f"===== Test Failed: {test_case_name} =====")
            self.base_utility.log_error(f"Reason: {e}")
            pytest.fail(str(e))

    # ---------------------------------------------------------------------
    # File Size Check
    # ---------------------------------------------------------------------

    def test_data_quality_file_size_check_for_inventory_data_xml_file(self):
        test_case_name = inspect.currentframe().f_code.co_name

        try:
            self.base_utility.log_info(f"===== Starting test: {test_case_name} =====")

            file_size_status = self.file_utility.check_file_size(
                "testData/inventory_data.xml"
            )

            logger.info(f"File Size Status : {file_size_status}")

            assert file_size_status, "inventory_data.xml is empty."

            self.base_utility.log_info(f"===== Test Passed: {test_case_name} =====")

        except Exception as e:
            self.base_utility.log_error(f"===== Test Failed: {test_case_name} =====")
            self.base_utility.log_error(f"Reason: {e}")
            pytest.fail(str(e))