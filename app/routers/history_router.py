from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from ..database import SessionLocal
from ..models import Purchase

router = APIRouter(prefix="/history")
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{email}", response_class=HTMLResponse)
def view_history(request: Request, email: str, db: Session = Depends(get_db)):
    purchases = db.query(Purchase).filter(
        Purchase.customer_email == email
    ).all()

    return templates.TemplateResponse("history.html", {
        "request": request,
        "purchases": purchases
    })


@router.get("/purchase/{purchase_id}", response_class=HTMLResponse)
def view_purchase(request: Request, purchase_id: int, db: Session = Depends(get_db)):
    purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()

    return templates.TemplateResponse("result.html", {
        "request": request,
        "purchase": purchase,
        "items": purchase.items,
        "total": purchase.total_amount,
        "balance": purchase.paid_amount - purchase.total_amount,
        "change": {"change_breakdown": {}, "remaining_unpaid": 0}
    })


@router.post("/redirect")
def redirect_to_history(
    history_email: str = Form(...)
):
    return RedirectResponse(f"/history/{history_email}", status_code=303)