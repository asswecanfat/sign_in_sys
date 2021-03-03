# import databases
from sqlalchemy import create_engine, MetaData, Table, Column, String
from func_set.config_read import ConfigReader
from sqlalchemy.orm import sessionmaker


DATABASE_URL = ConfigReader().get_database_URL()

engine = create_engine(
    'sqlite:///../data_file/test.db', connect_args={"check_same_thread": False},
    # echo=True,
)

# database = databases.Database(DATABASE_URL)

metadata = MetaData()


def creat_table(table_name: str) -> Table:
    return Table(table_name,
                 metadata,
                 Column("id", String(20), primary_key=True, unique=True),
                 Column("name", String(20)), )


def excle_exec(): ...


def table_get_inList():
    sm = sessionmaker(bind=engine)
    s = sm()
    a= []
    for i in engine.table_names():
        a.append(Table(i, metadata, autoload=True, autoload_with=engine))
    print(a)
    for i in a:

        s.execute(i.insert(), {'id': '561', 'name': 'asda'})
        s.commit()
    s.close()


if __name__ == '__main__':
    # metadata.create_all(engine, tables=[creat_table('test2', metadata)], checkfirst=True)
    table_get_inList()
