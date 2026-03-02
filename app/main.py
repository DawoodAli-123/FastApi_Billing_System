from fastapi import FastAPI
from .database import Base, engine, SessionLocal
from .routers import billing_router, product_router, history_router
from fastapi.staticfiles import StaticFiles
from . import models

app = FastAPI(title="Professional Billing System")

Base.metadata.create_all(bind=engine)

app.include_router(billing_router.router)
app.include_router(product_router.router)
app.include_router(history_router.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
# --------------------------
# Initial Data Seeding
# --------------------------

def seed_data():
    db = SessionLocal()

    # Seed products if empty
    if not db.query(models.Product).first():
        products = [
            models.Product(name="Laptop", stock=10, price=50000, tax_percentage=18),
            models.Product(name="Mouse", stock=50, price=500, tax_percentage=12),
            models.Product(name="Keyboard", stock=30, price=1500, tax_percentage=12),
        ]
        db.add_all(products)

    # Seed denominations if empty
    if not db.query(models.DenominationInventory).first():
        denominations = [
            2000, 500, 200, 100, 50, 20, 10
        ]
        for value in denominations:
            db.add(models.DenominationInventory(
                value=value,
                available_count=20
            ))

    db.commit()
    db.close()


seed_data()
