from pathlib import Path
from typing import List, Tuple, Dict
from datetime import datetime, timedelta
from collections import defaultdict

import aiofiles
from fastapi import Form, UploadFile, File, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy import Table

from dataSturct import Time
from database_op.sqlite3_op import table_get_inList_for_course_stu, get_session, build_table_in_DB, creat_course_table
from func_set.time_check import generate_deadline, check_time_outline, generate_fileTitle_time, get_last_time
from response import stu_form_reponses
from use_model import Mod_User
from . import routers_

deadline: datetime = ...
File_Filter: Tuple[str, str] = ('.jpg', '.png')
table_cache: List[Table] = ...
current_alive_table: Table = ...
base_file_path: Path = Path(__file__).parent.parent / Path('data_file')
current_alive_file_path: Path = ...
stu_data: Dict = ...
sign_cache: List = []
face_master: Dict = ...
mod_user = Mod_User()


@routers_.on_event("startup")
async def database_connect():
    global table_cache
    global stu_data
    global face_master
    table_cache, stu_table = table_get_inList_for_course_stu()
    session = next(get_session())

    raw_stu_data: List = session.query(stu_table).all()
    raw_stu_data.sort(key=lambda x: x[0])

    stu_data = dict(raw_stu_data)
    face_master = {
        stu[0]: num for num,
        stu in enumerate(
            raw_stu_data,
            start=1)}
    print(stu_data)
    print(face_master)


@routers_.get('/get_time', tags=['学生'])
async def get_time():
    sec = get_last_time(deadline) if isinstance(
        deadline, datetime) else timedelta()
    return {"status_code": 200, "second": sec}


@routers_.post('/stu_msg_upload', tags=['学生'],
               responses={**stu_form_reponses})
# @check_time_decorator(deadline=deadline)
async def get_stu_data(  # request: requests.Request,
        *,
        stu_name: str = Form(...,
                             regex=r'^[^\x00-\xff]+$',
                             description='学生姓名'),
        stu_id: str = Form(...,
                           regex=r'^\d{10}$',
                           description='学生学号'),
        pic: UploadFile = File(..., description='注意！是图片类型'),
        # UploadFile = File(..., description='需要验证的图片'),
        face: bytes = Body(..., description='图片文件转数组后的字节类型'),
        session: Session = Depends(get_session)):
    """
    发送学生的学号姓名表单, 且上传的文件是图片类型！！！

    - **stu_name**: 学生的姓名
    - **pic**: 图片文件
    """
    # print(request.headers)
    # if check_time(deadline):
    #     raise HTTPException(status_code=403, detail="拒绝访问")
    # print(Path(pic.filename).suffix.lower())
    global sign_cache
    if stu_data.get(stu_id, 'fake_name') != stu_name:
        raise HTTPException(status_code=402, detail="学生姓名错误！")
    if stu_id in sign_cache:
        raise HTTPException(status_code=400, detail="已签到！")
    if check_time_outline(deadline):
        raise HTTPException(status_code=404, detail="超时！拒绝访问")
    if Path(pic.filename).suffix.lower() not in File_Filter:
        raise HTTPException(status_code=403, detail="非图片类型")
    if not mod_user.recognize(face, face_master[stu_id]):
        raise HTTPException(status_code=405, detail="人脸验证失败！")
    async with aiofiles.open(f'{str(current_alive_file_path)}/{stu_name}.jpg',
                             'wb') as f:
        await f.write(await pic.read())
    session.execute(
        current_alive_table.insert(), {
            'name': stu_name,
            'pic_url': f'http://127.0.0.1:8000/static/{current_alive_file_path.name}/{stu_name}.jpg'})
    session.commit()
    sign_cache.append(stu_id)
    return {"status_code": 200, "detail": "签到成功！"}


@routers_.post('/start_signIn', tags=["教师"])
async def start(time: Time,
                course: str = Body(...,
                                   description="课程名")):
    """
    管理员开启签到接口
    - **seconds**: 持续秒数
    - **minutes**: 持续分钟数
    - **hours**: 持续小时数
    """
    global deadline
    global current_alive_table
    global current_alive_file_path
    global sign_cache
    global table_cache
    sign_cache.clear()
    try:
        current_alive_table = creat_course_table(course)
        table_cache.append(current_alive_table)
    except InvalidRequestError:
        raise HTTPException(status_code=403, detail=f"该表-{course}-已创建！")
    else:
        deadline = generate_deadline(seconds=time.seconds,
                                     minutes=time.minutes,
                                     hours=time.hours)
        build_table_in_DB(current_alive_table)
        current_alive_file_path = base_file_path / \
            Path(f'{generate_fileTitle_time()}-{course}')
        current_alive_file_path.mkdir()
    return {"status_code": 200}


@routers_.post('/stop_signIn', tags=["教师"])
async def stop_routine():
    """
    签到停止接口
    """
    global deadline
    deadline = generate_deadline()  # 默认为现在
    # print(deadline)
    # for table in table_cache:
    #     if table_name == table.name:
    #         return session.query(table).all()

    return {"status_code": 203}


@routers_.get('/excel_get', tags=["教师"])
async def creat_excel():
    return {"status_code": 200}


@routers_.get('/table_list_get', tags=["教师"])
async def get_table_list():
    return {
        "status_code": 200,
        "detail": [i.name for i in table_cache]}


@routers_.get('/get_table_data', tags=["教师"])
async def get_table_data(table_index: int, session: Session = Depends(get_session)):
    raw_table_data = session.query(table_cache[table_index]).all()
    axis = defaultdict(int)
    for i in raw_table_data:
        temp_data = i[3].strftime('%H-%M-%S')
        axis[temp_data] += 1
    return {"status_code": 200, "axis": axis}
