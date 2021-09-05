from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

engine = create_engine("sqlite:///../database/database.db", echo = True)
meta = MetaData()

lookup_table = Table(
    'lookup_table', meta,
    Column('id', Integer, primary_key = True),
    Column('table_name', String),
)

experiment = Table(
    'experiment1', meta,
    Column('variable1', String),
    Column('variable2', String),
    Column('variable3', String),
    Column('variable4', String),
    Column('variable5', String),
)

meta.create_all(engine)
