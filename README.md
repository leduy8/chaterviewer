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

## API documentation

```shell
http://localhost:8000/docs
```

## General flow

1. Transcribe incoming audio

2. Send to chatgpt and get response

3. Response will be audio generated by AI

4. Save chat history to send back and forth for context
