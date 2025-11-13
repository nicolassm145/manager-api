from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate

def create_item(db: Session, item_in: ItemCreate):
    existente = db.query(Item).filter(Item.sku == item_in.sku, Item.equipeId == item_in.equipeId).first()

    if existente:
        raise ValueError("SKU existente em outra equipe.")

    item = Item(**item_in.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_item(db: Session, item: Item, item_in: ItemUpdate):
    for field, value in item_in.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def delete_item(db: Session, item: Item):
    db.delete(item)
    db.commit()
    return True
