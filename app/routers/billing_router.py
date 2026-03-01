from fastapi import APIRouter, Request, BackgroundTasks, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from ..database import SessionLocal
from ..models import Product, DenominationInventory
from ..services.billing_service import generate_bill
from ..services.email_service import send_email_background

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
def billing_page(request: Request, db: Session = Depends(get_db)):
    from ..models import Product, DenominationInventory

    products = db.query(Product).all()
    denominations = db.query(DenominationInventory).all()

    return templates.TemplateResponse("billing.html", {
        "request": request,
        "products": products,
        "denominations": denominations
    })


from fastapi import HTTPException

@router.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    form_data = await request.form()

    customer_email = form_data.get("customer_email")
    paid_amount = float(form_data.get("paid_amount"))

    product_ids = form_data.getlist("product_ids")
    quantities = form_data.getlist("quantities")

    items = []
    for pid, qty in zip(product_ids, quantities):
        items.append({
            "product_id": int(pid),
            "quantity": int(qty)
        })

    # Update denomination inventory
    denoms = db.query(DenominationInventory).all()
    for denom in denoms:
        field = f"denom_{denom.value}"
        denom.available_count = int(form_data.get(field, 0))

    db.commit()

    try:
        result = generate_bill(db, customer_email, paid_amount, items)

        send_email_background(
            background_tasks,
            customer_email,
            f"Total: {result['total']}"
        )

        return templates.TemplateResponse("result.html", {
            "request": request,
            "purchase": result["purchase"],
            "items": result["items"],
            "total": result["total"],
            "balance": result["balance"],
            "change": result["change"],
            "success": "Invoice generated successfully"
        })

    except HTTPException as e:
        products = db.query(Product).all()
        denominations = db.query(DenominationInventory).all()

        return templates.TemplateResponse("billing.html", {
            "request": request,
            "products": products,
            "denominations": denominations,
            "error": e.detail
        })