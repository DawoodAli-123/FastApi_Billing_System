from sqlalchemy.orm import Session
from .. import models


def calculate_change(db: Session, balance: int):
    denominations = db.query(models.DenominationInventory).order_by(
        models.DenominationInventory.value.desc()
    ).all()

    change_given = {}
    remaining = balance

    for denom in denominations:
        if remaining <= 0:
            break

        max_notes = remaining // denom.value
        notes_to_give = min(max_notes, denom.available_count)

        if notes_to_give > 0:
            change_given[denom.value] = notes_to_give
            remaining -= denom.value * notes_to_give
            denom.available_count -= notes_to_give  # update inventory

    db.commit()

    return {
        "change_breakdown": change_given,
        "remaining_unpaid": remaining
    }