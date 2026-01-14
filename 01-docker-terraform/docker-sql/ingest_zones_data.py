#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
import click


def ingest_zones_data(url: str, engine, target_table: str):
    """
    Reads taxi zone data from the given URL and ingests it into the specified database table.
    """
    # Read the taxi zone data
    df = pd.read_csv(url)

    # Write the data to the database
    df.to_sql(
        name=target_table,
        con=engine,
        if_exists="replace",
        index=False
    )

    print(f"Table {target_table} created with {len(df)} records.")


@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL username')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='pgdatabase', help='PostgreSQL host')
@click.option('--pg-port', default='5432', help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--target-table', default='zones', help='Target table name')
def main(pg_user, pg_pass, pg_host, pg_port, pg_db, target_table):
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv'

    ingest_zones_data(
        url=url,
        engine=engine,
        target_table=target_table
    )


if __name__ == '__main__':
    main()