from pydantic import BaseModel, ConfigDict


class AddressBase(BaseModel):
    address_line: str
    city: str
    state: str
    postal_code: str
    country: str


class AddressCreate(AddressBase):
    pass


class AddressUpdate(AddressBase):
    pass


class AddressResponse(AddressBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)