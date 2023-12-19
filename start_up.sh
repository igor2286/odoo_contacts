export PYTHONPATH="odoo_contacts/"

python3 -m gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
