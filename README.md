## User & Address API
A boilerplate code for hex architecture
Very simple schema and API to get coordinates from user address

## Installation
Create a virtual environment
```shell
pip install virtualenv
virtualenv venv
```

Run virtual environtment(Windows)
```shell
venv\Scripts\activate
```

For Linux/MacOS
```shell
source env/bin/activate
```

Install requirements

```shell
pip install -r requirements.txt
```

To create the db
```shell
python src/adapter/schema.py
```

To start the server, run:

```shell
uvicorn src.router.router:app --reload
```

For docs of available API go to http://127.0.0.1:8000/docs
