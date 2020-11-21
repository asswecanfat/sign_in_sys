from .router.stu_routers import routers_
from fastapi import FastAPI


app = FastAPI()

app.include_router(routers_)
