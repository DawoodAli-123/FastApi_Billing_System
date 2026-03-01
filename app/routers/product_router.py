from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from ..database import SessionLocal
from ..models import Product

router = APIRouter(prefix="/products")
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
def list_products(request: Request, db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return templates.TemplateResponse("products.html", {
        "request": request,
        "products": products
    })


@router.post("/add")
def add_product(
    name: str = Form(...),
    stock: int = Form(...),
    price: float = Form(...),
    tax_percentage: float = Form(...),
    db: Session = Depends(get_db)
):
    db.add(Product(
        name=name,
        stock=stock,
        price=price,
        tax_percentage=tax_percentage
    ))
    db.commit()
    return RedirectResponse("/products", status_code=303)


from fastapi.responses import RedirectResponse

@router.post("/update/{product_id}")
def update_product(
    product_id: int,
    stock: int = Form(...),
    price: float = Form(...),
    tax_percentage: float = Form(...),
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product:
        product.stock = stock
        product.price = price
        product.tax_percentage = tax_percentage
        db.commit()

    return RedirectResponse("/products", status_code=303)


@router.post("/delete/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product:
        db.delete(product)
        db.commit()

    return RedirectResponse("/products", status_code=303)