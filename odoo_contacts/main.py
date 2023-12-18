import uvicorn
from fastapi import FastAPI
from pydantic_settings import SettingsConfigDict
from odoo_contacts.config import Settings
from odoo_contacts.core.router import router as router_contacts
from odoo_contacts.users.router import router as router_user
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# scheduler for background tasks
scheduler = AsyncIOScheduler()


def create_app():
    """Create fastapi app"""

    _app = FastAPI(title='Odoo Contacts')
    _app.include_router(router_user)
    _app.include_router(router_contacts)

    return _app


app = create_app()


@app.on_event("startup")
async def startup():
    """Start app job"""
    from odoo_contacts.cron_tasks import odoo_contacts
    scheduler.add_job(odoo_contacts, "interval", minutes=45)
    scheduler.start()


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
