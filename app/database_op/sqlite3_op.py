# import databases
from sqlalchemy import create_engine, MetaData, Table, Column, String, INTEGER
from func_set.config_read import ConfigReader
from sqlalchemy.orm import sessionmaker
from typing import List
from datetime import datetime


# 'sqlite:///../data_file/test.db'
DATABASE_URL = ConfigReader().get_database_URL()

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False},
    # echo=True,
)

# database = databases.Database(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata = MetaData()


def creat_stu_table(table_name: str) -> Table:
    """
    创建学生信息数据库表（此时未加入数据库）

    :param table_name: 表名
    :return: orm
    """
    return Table(table_name,
                 metadata,
                 Column("id", String(20), primary_key=True, unique=True),
                 Column("name", String(20)), )


def creat_course_table(course: str) -> Table:
    """
    创建课程数据库表（此时未加入数据库,名称以包含时间）

    :param course: 课程名称
    :return: orm
    """
    return Table(f'{str(datetime.now())}-{course}',
                 metadata,
                 Column("id",
                        INTEGER,
                        primary_key=True,
                        unique=True,
                        autoincrement=True),
                 Column("name", String(20)),
                 Column("pic_url", String(20))
                 )


def excle_exec(): ...


def build_table_in_DB(table: Table):
    """
    在数据库中建表

    :param table: 调用creat_table生成的表类
    :return:
    """
    metadata.create_all(engine, tables=[table], checkfirst=True)


def table_get_inList() -> List[Table]:
    """
    获取数据库中已有表

    :return:Table类型的list
    """
    table_list = []
    for table_name in engine.table_names():
        table_list.append(
            Table(
                table_name,
                metadata,
                autoload=True,
                autoload_with=engine))
    return table_list


def get_session():  # fastapi的依赖
    """
    fastapi的依赖

    :return: session
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


if __name__ == '__main__':
    # metadata.create_all(engine, tables=[creat_table('test2', metadata)], checkfirst=True)
    table_get_inList()
