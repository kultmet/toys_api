# toys_api

## GET START

clone the repository to your directory


```
cd /path_to_folder

git clone https://github.com/kultmet/toys_api.git
```

install [docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/linux/)

start app

```
# command line

docker-compose up -d

```


I wish you a pleasant use



In order to run tests you need to:

create and fill .env file
```
# .env

POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

go to /tests folder and run docker-compose

```
cd tests/
docker-compose up -d
```

go back to the root directory <code>cd ..</code>

run pytest by coverage

```
coverage run -m pytest
```

