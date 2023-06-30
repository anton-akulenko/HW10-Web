from datetime import datetime, timedelta

from fastapi import Depends
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import Contact
from src.schemas import ContactModel


async def get_all_contacts(db: Session):
    contacts = db.query(Contact).all()
    return contacts


async def get_contact_by_id(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def search_contacts_by_birthday(limit: int, offset: int, db: Session):
    today = datetime.today()
    current_year = today.year
    birthdays_in_period = []

    for contact in db.query(Contact).limit(limit).offset(offset).all():
        y, m, d, *_ = contact.birthday.split('-')
        contact_birthday = datetime(year=current_year, month=int(m), day=int(d))

        if today <= contact_birthday <= today + timedelta(days=7):
            birthdays_in_period.append(contact)
    return birthdays_in_period


async def create(body: ContactModel, db: Session = Depends(get_db)):
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    return contact


async def update(contact_id: int, body: ContactModel, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.additional_data = body.additional_data
        db.commit()
    return contact


async def remove(contact_id: int, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact
