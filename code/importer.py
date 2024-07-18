import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__, *[os.pardir] * 3)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'shopify.settings'
import django
django.setup()

import json
from customer.models import User, Customer, Address, Metafield, Blog, GiftCard, Event

filepath = './dummy-data/'

# Mengimpor data Customer
with open(filepath+'customer.json') as jsonfile:
    customers = json.load(jsonfile)
    for cust in customers:
        existUser = User.objects.filter(email=cust['email']).first()
        if existUser is None:
            user = User.objects.create_user(
                username=cust['email'],
                email=cust['email'],
                password=cust['password'],
                first_name=cust['first_name'],
                last_name=cust['last_name']
            )
            
            existCust = Customer.objects.filter(user=user).first()
            if existCust is None:
                Customer.objects.create(
                    user=user,
                    created_at=cust['created_at'],
                    updated_at=cust['created_at'],
                    state=cust['state'],
                    verified_email=cust['verified_email'],
                    send_email_wellcome=cust['send_email_wellcome'],
                    currency=cust['currency'],
                    phone=cust['phone']
                )

# Mengimpor data Address
with open(filepath+'address.json') as jsonfile:
    addresses = json.load(jsonfile)
    for num, adr in enumerate(addresses):
        addrExist = Address.objects.filter(id=num+1).first()
        if addrExist is None:
            Address.objects.create(
                customer_id=adr['customer'],
                address1=adr['address1'],
                address2=adr['address2'],
                city=adr['city'],
                province=adr['province'],
                country=adr['country'],
                company=adr['company'],
                phone=adr['phone'],
                zip=adr['zip'],
                default=adr['default']
            )

# Mengimpor data Metafield
with open(filepath+'metafield.json') as jsonfile:
    metafields = json.load(jsonfile)
    for meta in metafields:
        Metafield.objects.create(
            created_at=meta['created_at'],
            description=meta['description'],
            key=meta['key'],
            namespace=meta['namespace'],
            owner_id=meta['owner_id'],
            owner_resource=meta['owner_resource'],
            updated_at=meta['updated_at'],
            value=meta['value'],
            type=meta['type']
        )

with open(filepath + 'giftcard.json') as jsonfile:
    giftcards = json.load(jsonfile)
    for gift in giftcards:
        GiftCard.objects.create(
            api_client_id=gift['api_client_id'],
            balance=gift['balance'],
            code=gift['code'],
            created_at=gift['created_at'],
            currency=gift['currency'],
            customer_id=gift['customer_id'],
            disabled_at=gift['disabled_at'],
            expires_on=gift['expires_on'],
            id=gift['id'],
            initial_value=gift['initial_value'],
            last_characters=gift['last_characters'],
            line_item_id=gift['line_item_id'],
            note=gift['note'],
            order_id=gift['order_id'],
            template_suffix=gift['template_suffix'],
            user_id=gift['user_id'],
            updated_at=gift['updated_at'],
        )

# Mengimpor data Event
with open(filepath + 'Event.json') as jsonfile:
    events = json.load(jsonfile)
    for event in events:
        Event.objects.create(
            arguments=event['arguments'],
            body=event['body'],
            created_at=event['created_at'],
            id=event['id'],
            description=event['description'],
            path=event['path'],
            message=event['message'],
            subject_id=event['subject_id'],
            subject_type=event['subject_type'],
            verb=event['verb']
        )

# Mengimpor data Blog
with open(filepath + 'blogs.json') as jsonfile:
    blogs = json.load(jsonfile)
    for blog in blogs:
        Blog.objects.create(
            commentable=blog['commentable'],
            created_at=blog['created_at'],
            feedburner=blog['feedburner'],
            feedburner_location=blog['feedburner_location'],
            handle=blog['handle'],
            tags=blog['tags'],
            template_suffix=blog['template_suffix'],
            title=blog['title'],
            updated_at=blog['updated_at'],
            admin_graphql_api_id=blog['admin_graphql_api_id']
        )
