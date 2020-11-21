import databases
from sqlalchemy import create_engine, MetaData, Table, Column, String
from func_set.config_read import ConfigReader


DATABASE_URL = ConfigReader().get_database_URL()

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False},
    echo=True,
)

database = databases.Database(DATABASE_URL)

metadata = MetaData()


def creat_table(table_name: str, metadatas: MetaData) -> Table:
    return Table(table_name,
                 metadatas,
                 Column("id", String(20), primary_key=True, unique=True),
                 Column("name", String(20)), )


def excle_exec(): ...
