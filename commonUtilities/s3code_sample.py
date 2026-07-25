import pandas as pd
import boto3
from io import StringIO

# s3://bucket-employees-file/sources/sales_data.csv
# initiate a session with aws
s3  = boto3.client('s3')

def read_file_from_s3(bucket_name,file_key):
    # fetch a csv file from s3
    response = s3.get_object(Bucket=bucket_name,Key=file_key)

    csv_content = response['Body'].read().decode('utf-8')

    data = StringIO(csv_content)
    df = pd.read_csv(data)
    print(df)
    return df


def write_file_from_s3(df,bucket_name,file_key):
# convert the dataframe to CSV format
    csv_buffer = StringIO()
    df.to_csv(csv_buffer,index =False)
    s3.put_object(Bucket=bucket_name,Key=file_key,Body =csv_buffer.getvalue())


df = read_file_from_s3("bucket-employees-file","sources/sales_data.csv")
write_file_from_s3(df,"bucket-employees-file","sources/sales_data_target.csv")
