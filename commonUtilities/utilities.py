import pandas as pd
import cx_Oracle
from sqlalchemy import create_engine
import logging
from testConfiguration.etl_config import *
import pytest
import boto3
from io import StringIO
import paramiko
import os



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

class BaseUtility:
    # encapsulation
    def __read_file(self,file_path,file_type):
        if file_type == "csv":
            df = pd.read_csv(file_path)
        elif file_type == "json":
            df = pd.read_json(file_path)
        elif file_type == "xml":
            df = pd.read_xml(file_path,xpath=".//item")
        else:
            raise ValueError(f"unsupported file type pass{file_type}")
        return df

    def read_file_from_s3(self,bucket_name,file_key):
        try:
            logger.info("Reading file from S3 bucket")
            s3 = boto3.client('s3')
            response = s3.get_object(Bucket=bucket_name, Key=file_key)
            csv_content = response['Body'].read().decode('utf-8')
            data = StringIO(csv_content)
            df = pd.read_csv(data)
            logger.info(f"S3 data ia :{df}")
            return df
        except Exception as e:
            logger.error(f"S3 file read failed {e}")

    def linux_utility_download_file_from_linux_server(self):
        try:
            logger.info("Linux file download started..")
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(LINUX_HOSTNAME,username=LINUX_USERNAME,password=LINUX_PASSWORD)
            sftp = ssh_client.open_sftp()
            sftp.get(LINUX_REMOTE_FILE_PATH,LOCAL_FILE_PATH)
            sftp.close()
            logger.info("Linux file download completed..")
        except Exception as e :
            logger.error(f"Linux file download failed {e}")


    # abstraction
    def read_file(self,file_path,file_type):
        return self.__read_file(file_path,file_type)

    def log_info(self,message):
        logger.info(message)

    def log_error(self,message):
        logger.error(message)


class ValidationUtility(BaseUtility):
    #Polymorphism
    def execute_validation(self,validation_type,test_case_name,bucket_name=None,file_key=None,file_path=None,file_type=None,query_expected=None,db_expected=None,query_actual=None,db_actual=None):
        if validation_type == "FILE_TO_DB":
            self.validate_file_to_db(test_case_name,file_path,file_type,query_actual,db_actual)
        elif validation_type == "DB_TO_DB":
            self.validate_db_to_db(test_case_name,query_expected,db_expected,query_actual,db_actual)
        elif validation_type == "S3_TO_DB":
            self.validate_s3_to_db(test_case_name,bucket_name,file_key,query_actual,db_actual)

    def validate_file_to_db(self,test_case_name,file_path,file_type,query_actual,db_actual):
        try:
            df_expected = self.read_file(file_path,file_type)
            logger.info(f"expected data: {df_expected}")

            df_actual = pd.read_sql(query_actual,db_actual)
            logger.info(f"actual data: {df_actual}")

            # expected minus actual
            df_extra_expected= df_expected[~df_expected.apply(tuple,axis=1).isin(df_actual.apply(tuple,axis=1))]
            
            # actual minus expected
            df_extra_actual = df_actual[~df_actual.apply(tuple, axis=1).isin(df_expected.apply(tuple, axis=1))]

            # Create difference files only when differences exist
            if not df_extra_expected.empty or not df_extra_actual.empty:
                os.makedirs("differences", exist_ok=True)

                if not df_extra_expected.empty:
                    df_extra_expected.to_csv(
                        f"differences/extra_row_expected_{test_case_name}.csv",
                        index=False
                    )

                if not df_extra_actual.empty:
                    df_extra_actual.to_csv(
                        f"differences/extra_row_actual_{test_case_name}.csv",
                        index=False
                    )


            #assertion
            assert df_actual.equals(df_expected),f"{test_case_name} failed"
            logger.info(f"{test_case_name} passed")
        except Exception as e:
            logger.error(f"{test_case_name} validation failed :{e}")
            pytest.fail()


    def validate_db_to_db(self,test_case_name,query_expected,db_expected,query_actual,db_actual):
        try:
            df_expected = pd.read_sql(query_expected, db_expected).astype(str)
            logger.info(f"expected data: {df_expected}")

            df_actual = pd.read_sql(query_actual, db_actual).astype(str)
            logger.info(f"actual data: {df_actual}")

            # expected minus actual
            df_extra_expected = df_expected[~df_expected.apply(tuple, axis=1).isin(df_actual.apply(tuple, axis=1))]

            # actual minus expected
            df_extra_actual = df_actual[~df_actual.apply(tuple, axis=1).isin(df_expected.apply(tuple, axis=1))]

            # Create difference files only when differences exist
            if not df_extra_expected.empty or not df_extra_actual.empty:
                os.makedirs("differences", exist_ok=True)

                if not df_extra_expected.empty:
                    df_extra_expected.to_csv(
                        f"differences/extra_row_expected_{test_case_name}.csv",
                        index=False
                    )

                if not df_extra_actual.empty:
                    df_extra_actual.to_csv(
                        f"differences/extra_row_actual_{test_case_name}.csv",
                        index=False
                    )

            # assertion
            assert df_actual.equals(df_expected), f"{test_case_name} failed"
            logger.info(f"{test_case_name} passed")
        except Exception as e:
            logger.error(f"{test_case_name} validation failed :{e}")
            pytest.fail()



    def validate_s3_to_db(self,test_case_name,bucket_name,file_key,query_actual,db_actual):
        try:
            df_expected = self.read_file_from_s3(bucket_name,file_key)
            logger.info(f"expected data: {df_expected}")

            df_actual = pd.read_sql(query_actual, db_actual)
            logger.info(f"actual data: {df_actual}")


            # expected minus actual
            df_extra_expected= df_expected[~df_expected.apply(tuple,axis=1).isin(df_actual.apply(tuple,axis=1))]

            # actual minus expected
            df_extra_actual = df_actual[~df_actual.apply(tuple, axis=1).isin(df_expected.apply(tuple, axis=1))]

            # Create difference files only when differences exist
            if not df_extra_expected.empty or not df_extra_actual.empty:
                os.makedirs("differences", exist_ok=True)

                if not df_extra_expected.empty:
                    df_extra_expected.to_csv(
                        f"differences/extra_row_expected_{test_case_name}.csv",
                        index=False
                    )

                if not df_extra_actual.empty:
                    df_extra_actual.to_csv(
                        f"differences/extra_row_actual_{test_case_name}.csv",
                        index=False
                    )

            #assertion
            assert df_actual.equals(df_expected),f"{test_case_name} failed"
            logger.info(f"{test_case_name} passed")
        except Exception as e:
            logger.error(f"{test_case_name} validation failed :{e}")
            pytest.fail()

class SchemaValidation(BaseUtility):
    def validate_column_names(self,db_conn,table_name,expected_columns):
        query = f"select * from {table_name}"
        df = pd.read_sql(query,db_conn)
        actual_columns = list(df.columns)

        assert actual_columns == expected_columns,(
            f"\nColumn mismatch in table {table_name}"
            f"\nexpected columns :{expected_columns}"
            f"\nactual columns :{actual_columns}"
        )

    def validate_columns_dataTypes(self, db_conn, table_name, expected_datatypes):
        query = f"select * from {table_name}"
        df = pd.read_sql(query, db_conn)
        for column_name,allowed_datatypes in expected_datatypes.items():
            actual_data_type = df[column_name].dtype
            assert actual_data_type in allowed_datatypes,(
                f"\ndata type mismatch in table {table_name}"
                f"\n column :{column_name}"
                f"\nactual data type :{actual_data_type}"
                f"\nexpected data type :{allowed_datatypes}"
            )



