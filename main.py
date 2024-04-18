import asyncio
import os
from multiprocessing import Process

import uvicorn

from src.config import WEB_HOST, WEB_PORT


def uvicorn_run():
    uvicorn.run(app="src.main:app", host=WEB_HOST, port=int(WEB_PORT), log_level="info")


if __name__ == "__main__":
    os.system("alembic upgrade head")
    uvicorn_run()