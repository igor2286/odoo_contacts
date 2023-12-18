# Odoo Contacts
## Features

- Export data from Odoo every X minutes
- Update existed data in data base  
- Insert new data to data base  
- Delete unnecessary data from data base


## Tech
Dillinger uses a number of open source projects to work properly:

- FastApi - Framework for backend development
- SQLAlchemy - Library to manipulate with DB
- Odoo - ERP- и CRM-system to export data

## Installation

Create virtual environment  and  install dev dependencies

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
## Setup Enviroment variables
# Example
Create .env file in odoo_contacts and set environments variable
DB_HOST= db host  

DB_USER=db user  
DB_PASS=db password  
DB_NAME=db name  
DB_PORT=db port  
ODOO_URL=odoo url  
ODOO_DB=odoo db  
ODOO_USERNAME=odoo username  
ODOO_PASSWORD= odoo password  
SECRET_KEY=   
```sh
# Run this in terminal and insert value to SECRET_KEY 
openssl rand -hex 32
```  
ALGORITHM=Algoritm for crypt  
LOG_LEVEL=INFO

## Run alembic commands for creating tables in DB
```sh
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```  
## Rollback alembic revision if something went wrong
```sh
# If needed to rollback deeper use -2, -3 etc. instead -1
alembic downgrade -1
```  
## Start app
The uvicorn web server is used to run FastAPI. The command to run looks like this:
```
uvicorn app.main:app --reload