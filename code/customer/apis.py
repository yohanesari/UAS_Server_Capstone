import datetime
import json
from ninja import NinjaAPI, Query
from ninja.errors import HttpError
from ninja_simple_jwt.auth.views.api import mobile_auth_router
from ninja_simple_jwt.auth.ninja_auth import HttpJwtAuth
from .models import User, Customer, Address, Metafield, GiftCard, Event, Blog
from .schemas import CustomerOut, CustomerResp, AddressIn, AddressResp, AddressOut, CustomerIn, MetafieldSchema, MetafieldCreate, GiftCardIn, GiftCardOut, GiftCardResp, EventIn, EventOut, EventResp, BlogIn, BlogOut, BlogResp
from typing import List, Optional


api = NinjaAPI()
api.add_router("/auth/", mobile_auth_router)
apiAuth = HttpJwtAuth()

@api.get("hello")
def helloWorld(request):
    return {'hello': 'world'}

@api.get("customers.json", auth=apiAuth, response=CustomerResp)
def getAllCustomers(request, ids:str):
    int_ids = ids.split(',')
    customers = Customer.objects.filter(id__in=int_ids)
    return {'customers': customers}

# Single Customer
@api.get('customers/{id_cust}.json', auth=apiAuth, response=CustomerOut)
def getCustomerById(request, id_cust: int):
    customer = Customer.objects.get(pk=id_cust)
    return customer

# Searches for customers that match a supplied query
@api.get('customers/search.json', auth=apiAuth, response=CustomerResp)
def searchCustomers(request, query: str = Query(...), id_cust: int = None):
    email_query = query.split(':')[1] if 'email:' in query else None
    first_name_query = query.split(':')[1] if 'first_name:' in query else None
    last_name_query = query.split(':')[1] if 'last_name:' in query else None

    if email_query:
        customers = Customer.objects.filter(user__email=email_query)
    elif first_name_query:
        customers = Customer.objects.filter(user__first_name=first_name_query)
    elif last_name_query:
        customers = Customer.objects.filter(user__last_name=last_name_query)

    return {'customers': customers}


# Count all Customers
@api.get('customers/count.json', auth=apiAuth)
def countCustomers(request):
    customer_count = Customer.objects.count()
    return {"customer_count": customer_count}

# Update Customer
@api.put('customers/{id_cust}.json', auth=apiAuth, response=CustomerOut)
def updateCustomer(request, id_cust: int, data: CustomerIn):
    customer = Customer.objects.get(pk=id_cust)
    user = customer.user
    
    if data.email:
        user.email = data.email
    if data.first_name:
        user.first_name = data.first_name
    if data.last_name:
        user.last_name = data.last_name
    user.save()
    
    if data.phone:
        customer.phone = data.phone
    if data.state:
        customer.state = data.state
    if data.currency:
        customer.currency = data.currency
    customer.save()
    
    return customer

# Delete Customers
@api.delete('customers/{id_cust}.json')
def deleteCust(request, id_cust:int):
    Customer.objects.get(pk=id_cust).delete()
    return {}

# Add Address
@api.post('customers/{id_cust}/addresses.json', auth=apiAuth, response=AddressResp)
def addCustomer(request, id_cust:int, data:AddressIn):
    cust = Customer.objects.get(pk=id_cust)
    newAddr = Address.objects.create(
                customer=cust,
                address1=data.address1,
                address2=data.address2,
                city=data.city,
                province=data.province,
                company=data.company,
                phone=data.phone,
                zip=data.zip
            )
    return {"customer_address": newAddr}

# Retrieves a list of addresses for a customer
@api.get('customers/{id_cust}/addresses.json', auth=apiAuth, response=List[AddressOut])
def getCustomerAddresses(request, id_cust: int):
    addresses = Address.objects.filter(customer_id=id_cust)
    return addresses

# Retrieves details for a single customer address
@api.get('customers/{id_cust}/addresses/{id_addr}.json', auth=apiAuth, response=AddressResp)
def getCustomerAddress(request, id_cust: int, id_addr: int):
    try:
        address = Address.objects.get(customer_id=id_cust, id=id_addr)
        return {"customer_address": address}
    except Address.DoesNotExist:
        raise HttpError(404, "Address not found")

# Set Default Address
@api.put('customers/{id_cust}/addresses/{id_addr}/default.json', auth=apiAuth, response=AddressResp)
def setDefaultAddr(request, id_cust:int, id_addr:int):
    addr = Address.objects.get(pk=id_addr)
    addr.default =True
    addr.save()
    other = Address.objects.filter(customer_id=id_cust).exclude(id=id_addr)
    for data in other:
        data.default = False
        data.save()

    return {"customer_address": addr}

# Delete Address
@api.delete('customers/{id_cust}/addresses/{id_addr}.json')
def deleteAddr(request, id_cust:int, id_addr:int):
    Address.objects.get(pk=id_addr).delete()
    return {}

# Update Address
@api.put('customers/{id_cust}/addresses/{id_addr}.json', auth=apiAuth, response=AddressOut)
def updateCustomerAddress(request, id_cust: int, id_addr: int, data: AddressIn):
    address = Address.objects.get(pk=id_addr, customer_id=id_cust)
    address.address1 = data.address1
    address.address2 = data.address2
    address.city = data.city
    address.province = data.province
    address.company = data.company
    address.phone = data.phone
    address.zip = data.zip
    address.save()
    return address

#Metafield

def load_dummy_metafields():
    with open("dummy-data/metafield.json", "r") as f:
        return json.load(f)

# Retrieve Metafields by owner_id
@api.get("blogs/{owner_id}/metafields.json", response=dict)
def RetrieveMetafieldbyOwnerId(request, owner_id: int):
    DUMMY_METAFIELDS = load_dummy_metafields()
    try:
        metafield = next(item for item in DUMMY_METAFIELDS if item["owner_id"] == owner_id)
        metafield_data = {
            "metafields": [{
                "namespace": metafield["namespace"],
                "key": metafield["key"],
                "value": metafield["value"],
                "description": metafield["description"],
                "owner_id": metafield["owner_id"],
                "created_at": metafield["created_at"],
                "updated_at": metafield["updated_at"],
                "owner_resource": metafield["owner_resource"],
                "type": metafield["type"],
                "admin_graphql_api_id": f"gid://shopify/Metafield/{metafield['id']}"
            }]
        }
        return metafield_data
    except StopIteration:
        raise HttpError(404, "Metafield not found")
  
# Count Metafields by owner_id
@api.get('blogs/{owner_id}/metafields/count.json', auth=apiAuth)
def countMetafields(request, owner_id: int):
    metafield_count = Metafield.objects.filter(owner_id=owner_id).count()
    return {"metafield_count": metafield_count}

# Retrieve a specific Metafield by owner_id and metafield_id
@api.get("blogs/{owner_id}/metafields/{metafield_id}.json", response=dict)
def RetrievespecificMetafield(request, owner_id: int, metafield_id: int):
    DUMMY_METAFIELDS = load_dummy_metafields()
    try:
        metafield = next(
            item for item in DUMMY_METAFIELDS 
            if item["owner_id"] == owner_id and item["id"] == metafield_id
        )
        metafield_data = {
            "namespace": metafield["namespace"],
            "key": metafield["key"],
            "value": metafield["value"],
            "description": metafield["description"],
            "owner_id": metafield["owner_id"],
            "created_at": metafield["created_at"],
            "updated_at": metafield["updated_at"],
            "owner_resource": metafield["owner_resource"],
            "type": metafield["type"],
            "admin_graphql_api_id": f"gid://shopify/Metafield/{metafield['id']}"
        }
        return metafield_data
    except StopIteration:
        raise HttpError(404, "Metafield not found")

# Retrieve all Metafields
@api.get("blogs/metafields.json", response=List[dict])
def AllMetafields(request):
    DUMMY_METAFIELDS = load_dummy_metafields()
    all_metafields = [
        {
            "namespace": metafield["namespace"],
            "key": metafield["key"],
            "value": metafield["value"],
            "description": metafield["description"],
            "owner_id": metafield["owner_id"],
            "created_at": metafield["created_at"],
            "updated_at": metafield["updated_at"],
            "owner_resource": metafield["owner_resource"],
            "type": metafield["type"],
            "admin_graphql_api_id": f"gid://shopify/Metafield/{metafield['id']}"
        }
        for metafield in DUMMY_METAFIELDS
    ]
    return all_metafields

# Retrieve Metafields with query parameters
@api.get('blogs/{owner_id}/metafields/search.json', auth=apiAuth, response=List[MetafieldSchema])
def searchMetafields(request, owner_id: int, query: str = Query(...)):
    
    key_query = query.split(':')[1] if 'key:' in query else None
    namespace_query = query.split(':')[1] if 'namespace:' in query else None
    description_query = query.split(':')[1] if 'description:' in query else None

    if key_query:
        metafields = Metafield.objects.filter(owner_id=owner_id, key=key_query)
    elif namespace_query:
        metafields = Metafield.objects.filter(owner_id=owner_id, namespace=namespace_query)
    elif description_query:
        metafields = Metafield.objects.filter(owner_id=owner_id, description=description_query)
    else:
        metafields = Metafield.objects.filter(owner_id=owner_id)

    return metafields

# Create a new Metafield
@api.post("blogs/{owner_id}/metafields.json", auth=apiAuth, response=MetafieldSchema)
def createMetafield(request, owner_id: int, payload: MetafieldCreate):
    metafield = Metafield.objects.create(
        owner_id=owner_id,
        namespace=payload.namespace,
        key=payload.key,
        value=payload.value,
        description=payload.description,
        owner_resource=payload.owner_resource,
        type=payload.type
    )
    return metafield

# Update a metafield
@api.put('blogs/{owner_id}/metafields/{metafield_id}.json', auth=apiAuth, response=MetafieldSchema)
def updateMetafield(request, owner_id: int, metafield_id: int, data: MetafieldSchema):
        metafield = Metafield.objects.get(owner_id=owner_id, id=metafield_id)
        metafield.key = data.key
        metafield.value = data.value
        metafield.namespace = data.namespace
        metafield.description = data.description
        metafield.type = data.type
        metafield.updated_at = datetime.now()
        metafield.save()

        return metafield

# Delete a metafield
@api.delete('blogs/{owner_id}/metafields/{metafield_id}.json', auth=apiAuth)
def deleteMetafield(request, owner_id: int, metafield_id: int):
    try:
        metafield = Metafield.objects.get(owner_id=owner_id, id=metafield_id)
        metafield.delete()
        return {"message": "Metafield deleted successfully"}
    except Metafield.DoesNotExist:
        raise HttpError(404, "Metafield not found")
    except Exception as e:
        raise HttpError(400, f"Failed to delete metafield: {str(e)}")

#Blog
@api.post("blogs.json", response=BlogOut)
def create_blog(request, payload: BlogIn):
    blog = Blog.objects.create(**payload.dict())
    return blog

@api.get("blogs.json", response=List[BlogOut])
def list_blogs(request):
    blogs = Blog.objects.all()
    return blogs

@api.get("blogs/{blog_id}.json", response=BlogOut)
def get_blog(request, blog_id: int):
    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        raise HttpError(404, f"Blog with id {blog_id} not found")
    return blog

@api.get("blogs/count.json", response=int)
def count_blogs(request):
    return Blog.objects.count()

@api.put("blogs/{blog_id}.json", response=BlogOut)
def update_blog(request, blog_id: int, payload: BlogIn):
    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        raise HttpError(404, f"Blog with id {blog_id} not found")

    for attr, value in payload.dict().items():
        setattr(blog, attr, value)
    blog.save()
    return blog

@api.delete("blogs/{blog_id}.json")
def delete_blog(request, blog_id: int):
    try:
        blog = Blog.objects.get(id=blog_id)
        blog.delete()
        return {"success": True}
    except Blog.DoesNotExist:
        raise HttpError(404, f"Blog with id {blog_id} not found")

#GIFTCARD

#create 
@api.post("giftcards.json", auth=apiAuth, response=GiftCardResp)
def create_gift_card(request, data: GiftCardIn):
    gift_card = GiftCard.objects.create(**data.dict())
    return {"giftcard": gift_card}

#create
@api.post("giftcards/{gift_card_id}/disable.json", auth=apiAuth, response=GiftCardResp)
def disable_gift_card(request, gift_card_id: int):
    try:
        gift_card = GiftCard.objects.get(pk=gift_card_id)
        gift_card.disabled_at = datetime.now()
        gift_card.save()
        return {"giftcard": gift_card}
    except GiftCard.DoesNotExist:
        raise HttpError(404, "Gift card not found")

#retrive list giftcard
@api.get("giftcards.json", auth=apiAuth, response=List[GiftCardOut])
def list_gift_cards(request):
    gift_cards = GiftCard.objects.all()
    return gift_cards

#Retrieve spesific giftcard
@api.get("giftcards/{gift_card_id}.json", auth=apiAuth, response=GiftCardOut)
def retrieve_gift_card(request, gift_card_id: int):
    try:
        gift_card = GiftCard.objects.get(id=gift_card_id)
        return gift_card
    except GiftCard.DoesNotExist:
        raise HttpError(404, "Gift card not found")

#Count GiftCard by Id
@api.get('customers/{id_cust}/gift_cards/count.json', auth=apiAuth)
def countGiftCard(request, id_cust: int):
    giftcard_count = GiftCard.objects.filter(customer_id=id_cust).count()
    return {"giftcard_count": giftcard_count}

#Retrieve search a giftcards
@api.get("giftcards/search.json", auth=apiAuth, response=List[GiftCardOut])
def search_gift_cards(request, query: str = Query(None)):
    if query:
        gift_cards = GiftCard.objects.filter(last_characters__icontains=query)
    else:
        gift_cards = GiftCard.objects.all()
    return gift_cards

#Update GiftCard
@api.put("giftcards/{gift_card_id}.json", auth=apiAuth, response=GiftCardOut)
def update_gift_card(request, gift_card_id: int, data: GiftCardIn):
    try:
        gift_card = GiftCard.objects.get(pk=gift_card_id)
        for attr, value in data.dict().items():
            setattr(gift_card, attr, value)
        gift_card.save()
        return gift_card
    except GiftCard.DoesNotExist:
        raise HttpError(404, "Gift card not found")
    
#Event

#Retrieve a list of event
@api.get('events.json', response=List[EventOut])
def list_events(request):
    events = Event.objects.all()
    return events

#retrieve a spesific of event
@api.get('events/{event_id}.json', response=EventOut)
def get_event(request, event_id: int):
    event = Event.objects.get(id=event_id)
    return event

#retrieve a count of event
@api.get('events/count.json', response=int)
def count_events(request):
    count = Event.objects.count()
    return count