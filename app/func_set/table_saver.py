from sqlalchemy import Table
from datetime import datetime
# from heapq import *  # 启用堆排序
# from typing import List


# table类节点，用于堆排序
class TableSaveNode(object):
    __slots__ = ['table_name', 'table', 'node_creat_time']

    def __init__(self,
                 table_name: str,
                 tabel: Table):
        self.table_name = table_name
        self.table = tabel
        self.node_creat_time = datetime.now().timestamp()

    def __lt__(self, other):
        return self.node_creat_time < other.node_creat_time

    def __str__(self):
        return f'time:{self.node_creat_time}'

    __repr__ = __str__


# import random
# from time import sleep
# from pprint import pprint
#
#
# def tree(heap: List):  # , table_node: TableSaveNode
#
#     for i in range(10):
#         sleep(random.randint(0, 1))
#         heappush(heap, TableSaveNode(str(i), Table()))
#
#
# if __name__ == '__main__':
#     heap = []
#     tree(heap)
#     pprint(heap)
