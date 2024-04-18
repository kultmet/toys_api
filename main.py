import os

import uvicorn

from src.config import DB_HOST, WEB_HOST, WEB_PORT


def uvicorn_run():
    uvicorn.run(app="src.main:app", host=WEB_HOST, port=int(WEB_PORT), log_level="info")


if __name__ == "__main__":
    print(DB_HOST)
    os.system("alembic upgrade head")
    uvicorn_run()
