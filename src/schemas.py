from pydantic import BaseModel, EmailStr, Field


class ContactModel(BaseModel):
    first_name: str = Field('John', min_length=3, max_length=16)
    last_name: str = Field('Week', min_length=3, max_length=16)
    email: EmailStr
    phone_number: str = Field('+31112222222', min_length=9, max_length=16)
    birthday: str = Field('1970-05-05')
    additional_data: str


class ContactResponse(BaseModel):
    id: int = 1
    first_name: str #= Field('John', min_length=3, max_length=16)
    last_name: str #= Field('Week', min_length=3, max_length=16)
    email: EmailStr
    phone_number: str #= Field('+31112222222', min_length=9, max_length=16)
    birthday: str #= Field('1970-05-05')
    additional_data: str

    class Config:
        orm_mode = True
