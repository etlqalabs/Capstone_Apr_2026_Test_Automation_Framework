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


    # abstraction
    def read_file(self,file_path,file_type):
        return self.__read_file(file_path,file_type)

    def log_info(self,message):
        logger.info(message)

    def log_error(self,message):
        logger.error(message)

