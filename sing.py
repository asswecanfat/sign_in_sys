# -*- coding: utf-8 -*-

import json
import re
import chardet
import asyncio
from pathlib import Path


PATTERN = r'\[([0-9]{2}\:[0-9]{2})\.[0-9]{2}\](.+)'


async def comprea2get_data(pattern: str, context: str) -> list:
    prog = re.compile(pattern, re.ASCII)
    return prog.findall(context)


def check_file_code(file: str) -> str:
    with open(file, 'rb') as f:
        data = f.read()
        result = chardet.detect(data)
        return result['encoding']


async def read_file(song_file: str):
    with open(song_file, 'r', encoding=check_file_code(song_file)) as f:
        context = f.read()
        data = await comprea2get_data(PATTERN, context)
        singer = await comprea2get_data(r'\[ar\:(.+)\]', context)
        song_title = await comprea2get_data(r'\[ti\:(.+)\]', context)
        file_name = f'{singer[0]} - {song_title[0]}'
        print(json.dumps(dict(data), ensure_ascii=False))
        with open(Path(__file__).parent / '') as fo:
            ...


if __name__ == '__main__':
    asyncio.run(read_file(r'C:\Users\10248\Desktop\lrc\BEYOND - 灰色轨迹.lrc'))