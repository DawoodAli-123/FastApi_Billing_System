from sqlalchemy.orm import Session
from fastapi import HTTPException
from .. import models
from .denomination_service import calculate_change


def calculate_line_total(price: float, tax: float, quantity: int) -> float:
    subtotal = price * quantity
    tax_amount = subtotal * (tax / 100)
    return round(subtotal + tax_amount, 2)


def generate_bill(db: Session, customer_email: str, paid_amount: float, items: list):
    total_amount = 0
    purchase_items = []

    # 1️⃣ Validate products and stock
    for item in items:
        product = db.query(models.Product).filter(models.Product.id == item["product_id"]).first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if item["quantity"] > product.stock:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {product.name}"
            )

        line_total = calculate_line_total(
            product.price,
            product.tax_percentage,
            item["quantity"]
        )

        total_amount += line_total

        purchase_items.append({
            "product": product,
            "quantity": item["quantity"],
            "line_total": line_total
        })

    total_amount = round(total_amount, 2)

    # 2️⃣ Validate paid amount
    if paid_amount < total_amount:
        raise HTTPException(
            status_code=400,
            detail="Paid amount is less than total bill amount"
        )

    balance = round(paid_amount - total_amount, 2)

    # 3️⃣ Calculate change using available denominations
    change_result = calculate_change(db, int(balance))

    # 4️⃣ Create purchase record
    purchase = models.Purchase(
        customer_email=customer_email,
        total_amount=total_amount,
        paid_amount=paid_amount
    )
    db.add(purchase)
    db.commit()
    db.refresh(purchase)

    # 5️⃣ Save purchase items & reduce stock
    for item in purchase_items:
        db.add(models.PurchaseItem(
            purchase_id=purchase.id,
            product_id=item["product"].id,
            quantity=item["quantity"],
            line_total=item["line_total"]
        ))

        item["product"].stock -= item["quantity"]

    db.commit()

    return {
        "purchase": purchase,
        "items": purchase_items,
        "total": total_amount,
        "balance": balance,
        "change": change_result
    }