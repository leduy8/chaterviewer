# Fastapi project template

## Requirements

- Python 3.8+
- PostgreSQL, MySQL or SQLite

## Installation

### Set up virtual environment

```shell
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies

```shell
pip install -r common.txt
```

### Install `pre-commit` hooks

- Install `pre-commit`: https://pre-commit.com/
- Install `pre-commit` hooks:

```shell
pre-commit install
```

## Running

Inside the virtual environment, run

```shell
uvicorn main:app --reload
```
