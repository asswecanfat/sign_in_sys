# import databases
from sqlalchemy import create_engine, MetaData, Table, Column, String, INTEGER, DateTime
from func_set.config_read import ConfigReader
from sqlalchemy.orm import sessionmaker
from typing import List, Generator
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


def creat_stu_table() -> Table:
    """
    创建学生信息数据库表（此时未加入数据库）

    :return: orm
    """
    return Table("student",
                 metadata,
                 Column("id", String(20), primary_key=True, unique=True),
                 Column("name", String(20)), )


def creat_course_table(course: str) -> Table:
    """
    创建课程数据库表（此时未加入数据库,名称以包含时间）

    :param course: 课程名称
    :return: orm
    """
    return Table(f'{str(datetime.now().strftime("%Y-%m-%d %H-%M"))}-{course}',
                 metadata,
                 Column("id",
                        INTEGER,
                        primary_key=True,
                        unique=True,
                        autoincrement=True),
                 Column("name", String(20)),
                 Column("pic_url", String(20)),
                 Column("signIn_time", DateTime, default=datetime.now)
                 )


def excle_exec(): ...


def build_table_in_DB(new_table: Table):
    """
    在数据库中建表

    :param new_table: 调用creat_table生成的表类
    :return:
    """
    metadata.create_all(engine, tables=[new_table], checkfirst=True)


def table_get_inList_for_course_stu() -> (List[Table], Table):
    """
    获取数据库中已有表

    :return:Table类型的list
    """
    table_list = []
    stu_table = None
    for table_name in engine.table_names():
        table = Table(
            table_name,
            metadata,
            autoload=True,
            autoload_with=engine)
        if table_name != 'student':
            table_list.append(table)
        else:
            stu_table = table
    return table_list, stu_table


def get_session() -> Generator:  # fastapi的依赖
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
    f_table = creat_stu_table()
    build_table_in_DB(f_table)
