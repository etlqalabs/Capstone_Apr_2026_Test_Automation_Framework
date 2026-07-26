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


@pytest.fixture()
def connect_to_oracle_database():
    logger.info("Oracle database connection being established..")
    oracle_conn = create_engine(
        f"oracle+cx_oracle://{ORACLE_USER}:{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}").connect()
    logger.info("Oracle database connection has been established..")
    yield oracle_conn
    oracle_conn.close()
    logger.info("Oracle database connection has been terminated..")


@pytest.fixture()
def connect_to_mysql_database():
    logger.info("mysql database connection being established..")
    mysql_conn = create_engine(
        F"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}").connect()
    logger.info("mysql database connection has been established..")
    yield mysql_conn
    mysql_conn.close()
    logger.info("mysql database connection has been terminated..")
