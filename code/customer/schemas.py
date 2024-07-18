from ninja import Schema, Field
from datetime import datetime
from typing import Optional, List
from pydantic import model_validator

from customer.models import Customer, Address, Metafield, GiftCard, Event, Blog

class AddressIn(Schema):
    customer_id: int
    address1: str
    address2: Optional[str] = ''
    city: str
    first_name: Optional[str] = ''
    last_name: Optional[str] = ''
    phone: Optional[str] = ''
    province: str
    country: str
    zip: str
    company: str
    name: Optional[str] = ''

class AddressOut(Schema):
    id: int
    customer_id: int
    first_name: str = Field(alias='customer.user.first_name')
    last_name: str = Field(alias='customer.user.last_name')
    company: str
    address1: str
    address2: str
    city: str
    province: str
    zip: str
    phone: Optional[str] = ''
    name: str
    default: bool

class AddressResp(Schema):
    customer_address: AddressOut

class CustomerOut(Schema):
    id: int
    email: str = Field(alias='user.email')
    created_at: datetime
    updated_at: datetime
    first_name: str = Field(alias='user.first_name')
    last_name: str = Field(alias='user.last_name')
    order_counts: int
    state: str
    verified_email: bool
    currency: str
    phone: str
    addresses: Optional[List[AddressOut]] = Field(alias='address_set')

class CustomerIn(Schema):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    state: Optional[str] = None
    phone: Optional[str] = None
    currency: Optional[str] = None

class CustomerResp(Schema):
    customers: List[CustomerOut]

class MetafieldSchema(Schema):
    id: int
    created_at: datetime
    description: Optional[str] = None
    key: str
    namespace: str
    owner_id: int
    owner_resource: str
    updated_at: datetime
    value: str
    type: str

class MetafieldCreate(Schema):
    description: Optional[str] = None
    key: str
    namespace: str
    owner_id: int
    owner_resource: str
    value: str
    type: str

class GiftCardIn(Schema):
    api_client_id: Optional[int] = None
    balance: float
    code: str
    created_at: datetime
    currency: str
    customer_id: Optional[int] = None
    disabled_at: Optional[datetime] = None
    expires_on: Optional[datetime] = None
    initial_value: float
    last_characters: str
    line_item_id: Optional[int] = None
    note: Optional[str] = ''
    order_id: Optional[int] = None
    template_suffix: Optional[str] = ''
    user_id: Optional[int] = None
    updated_at: datetime

class GiftCardOut(Schema):
    id: int
    api_client_id: Optional[int] = None
    balance: float
    code: str
    created_at: datetime
    currency: str
    customer_id: Optional[int] = None
    disabled_at: Optional[datetime] = None
    expires_on: Optional[datetime] = None
    initial_value: float
    last_characters: str
    line_item_id: Optional[int] = None
    note: Optional[str] = ''
    order_id: Optional[int] = None
    template_suffix: Optional[str] = ''
    user_id: Optional[int] = None
    updated_at: datetime

class GiftCardResp(Schema):
    giftcard: GiftCardOut


class EventIn(Schema):
    arguments: List[str]
    body: Optional[str] = None
    created_at: datetime
    id: int
    description: str
    path: str
    message: str
    subject_id: int
    subject_type: str
    verb: str

class EventOut(Schema):
    arguments: List[str]
    body: Optional[str] = None
    created_at: datetime
    id: int
    description: str
    path: str
    message: str
    subject_id: int
    subject_type: str
    verb: str

class EventResp(Schema):
    event: EventOut

class BlogIn(Schema):
    commentable: str
    created_at: datetime
    feedburner: Optional[str] = None
    feedburner_location: Optional[str] = None
    handle: str
    tags: str
    template_suffix: Optional[str] = None
    title: str
    updated_at: datetime
    admin_graphql_api_id: str

class BlogOut(Schema):
    id: int
    commentable: str
    created_at: datetime
    feedburner: Optional[str] = None
    feedburner_location: Optional[str] = None
    handle: str
    tags: str
    template_suffix: Optional[str] = None
    title: str
    updated_at: datetime
    admin_graphql_api_id: str

class BlogResp(Schema):
    blog: BlogOut
