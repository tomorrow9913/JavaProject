# Java Project

Kiosk Projet


## requirements

if you don't have a miniconda(or anaconda), you can install it on this url.
https://docs.anaconda.com/free/miniconda/index.html

```
conda create -n secure_coding python=3.9
conda activate secure_coding
pip install -r requirements.txt
```

## usage



```
uvicorn fastapi_app:app --reload
```

or 

```
python fastapi_app.py
```


## Structure

- `core`: database connection, models and oauth configuration
- `crud`: CRUD operations for each table
- `routes`: API routes
- `schema`: Pydantic models for request and response
- `utils`: utility functions