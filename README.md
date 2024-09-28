# cold-start-backend

Web API wrapper for the module - backend part

### [Module](https://github.com/digital-fracture/cold-start)
#### [Documentation](https://digital-fracture.github.io/cold-start)

### [Website](https://card-mu-lyart.vercel.app/)

### [Folder with notebooks and other sources](https://drive.google.com/drive/folders/1_mlXCOj2t3n2GSYQgjePXLy0It9COIET?usp=sharing)


## Run by yourself

### Python package is available at [PyPI](https://pypi.org/project/rutube-cold-start)

### Docker Compose

```shell
git clone https://github.com/digital-fracture/cold-start-backend.git
cd cold-start-backend

touch .env  # you will need to declare variables listed below

docker compose up -d
```

Needed variables:
- `POSTGRES_HOST`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `NGROK_AUTHTOKEN`
- `NGROK_URL`


## Stack

- [python 3.11](https://python.org) - programming language
- [cold-start](https://pypi.org/project/cold-start) - ML processor
- [FastAPI](https://pypi.org/project/fastapi) - web server engine
- [SQLAlchemy](https://pypi.org/project/SQLAlchemy/) - database engine (**PostgreSQL**)
- [Docker Compose](https://docs.docker.com/compose/) - deployment tool
- And more
