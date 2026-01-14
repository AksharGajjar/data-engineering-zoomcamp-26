#!/usr/bin/env python
# coding: utf-8

import os
import urllib.request
import pandas as pd
from sqlalchemy import create_engine
import pyarrow.parquet as pq
from tqdm.auto import tqdm
import click
import psycopg2.extras

def psql_insert_copy(table, conn, keys, data_iter):
    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:
        quoted_keys = [f'"{key}"' for key in keys]
        
        sql = f"INSERT INTO {table.table} ({', '.join(quoted_keys)}) VALUES %s"
        psycopg2.extras.execute_values(cur, sql, list(data_iter))

def ingest_data(
        url: str,
        engine,
        target_table: str,
        chunksize: int = 100000
):
    file_name = url.split('/')[-1]
    print(f"Downloading {url} to {file_name}...")
    
    try:
        urllib.request.urlretrieve(url, file_name)
        print("Download complete.")
    except Exception as e:
        print(f"Download failed: {e}")
        return

    print(f"Opening Parquet file: {file_name}")
    
    try:
        parquet_file = pq.ParquetFile(file_name)
    except FileNotFoundError:
        print(f"Error: File {file_name} not found.")
        return

    batch_iter = parquet_file.iter_batches(batch_size=chunksize)
    
    try:
        first_batch = next(batch_iter)
        first_df = first_batch.to_pandas()

        first_df.head(0).to_sql(
            name=target_table,
            con=engine,
            if_exists="replace",
            index=False
        )
        print(f"Table {target_table} created")

        first_df.to_sql(
            name=target_table,
            con=engine,
            if_exists="append",
            method=psql_insert_copy,
            index=False 
        )
        print(f"Inserted first chunk: {len(first_df)}")
        
    except StopIteration:
        print("The parquet file is empty.")
        return

    for batch in tqdm(batch_iter):
        df_chunk = batch.to_pandas()
        
        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists="append",
            method=psql_insert_copy,
            index=False 
        )

    print(f'Done ingesting to {target_table}')

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL username')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='pgdatabase', help='PostgreSQL host')
@click.option('--pg-port', default='5432', help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--year', default=2025, type=int, help='Year of the data')
@click.option('--month', default=11, type=int, help='Month of the data')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for ingestion')
@click.option('--target-table', default='green_taxi_data', help='Target table name')
def main(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, chunksize, target_table):
    
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    
    url_prefix = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
    url = f'{url_prefix}/green_tripdata_{year:04d}-{month:02d}.parquet'

    ingest_data(
        url=url,
        engine=engine,
        target_table=target_table,
        chunksize=chunksize
    )

if __name__ == '__main__':
    main()