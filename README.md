# Stack Overflow Clone

A simple Stack Overflow clone with Flask.

## Getting Started

- Clone the repo

- Create a virtual env `python3 -m venv venv` and activate `. venv/bin/activate`

- Install dependecies `pip install -r requirements.txt`

- Create a **.env** file and add values from **.env_example**

- Source the environment variables `source .env`

- Run migrations `flask db upgrade`

- Start server locally `flask run` or `python main.py`

- Run tests `pytest --cov`

## Tools

- Flask

- Postgres
