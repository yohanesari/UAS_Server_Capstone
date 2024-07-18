from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    STATE_CHOICE = [
        ('disabled', 'disabled'),
        ('invited', 'invited'),
        ('enabled', 'enabled'),
        ('declined', 'declined')
    ]

    user = models.OneToOneField(User, on_delete=models.RESTRICT)
    phone = models.CharField(max_length=100, null=True, blank=True)
    verified_email = models.BooleanField(default=False)
    send_email_welcome = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=20, choices=STATE_CHOICE)
    currency = models.CharField(max_length=10)

    @property
    def order_counts(self):
        return 0

class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address1 = models.TextField()
    address2 = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=250)
    province = models.CharField(max_length=250)
    country = models.CharField(max_length=250)
    phone = models.CharField(max_length=100, null=True, blank=True)
    zip = models.CharField(max_length=20)
    company = models.CharField(max_length=200, null=True, blank=True)
    default = models.BooleanField(default=False)

    @property
    def name(self):
        return f"{self.customer.user.first_name} {self.customer.user.last_name}"

class Metafield(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    key = models.CharField(max_length=64)
    namespace = models.CharField(max_length=255)
    owner_id = models.BigIntegerField()
    owner_resource = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    value = models.TextField()
    type = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.namespace}:{self.key}'

    class Meta:
        unique_together = ('namespace', 'key', 'owner_id', 'owner_resource')

class GiftCard(models.Model):
    api_client_id = models.BigIntegerField(null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    code = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    currency = models.CharField(max_length=10)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    disabled_at = models.DateTimeField(null=True, blank=True)
    expires_on = models.DateField(null=True, blank=True)
    initial_value = models.DecimalField(max_digits=10, decimal_places=2)
    last_characters = models.CharField(max_length=4)
    line_item_id = models.BigIntegerField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    order_id = models.BigIntegerField(null=True, blank=True)
    template_suffix = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

class Event(models.Model):
    arguments = models.JSONField()
    body = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField()
    id = models.BigIntegerField(primary_key=True)
    description = models.TextField()
    path = models.CharField(max_length=255)
    message = models.TextField()
    subject_id = models.BigIntegerField()
    subject_type = models.CharField(max_length=50)
    verb = models.CharField(max_length=50)

    def __str__(self):
        return f"Event {self.id} - {self.description}"
    
class Blog(models.Model):
    commentable = models.CharField(max_length=3, choices=[('yes', 'yes'), ('no', 'no')], default='no')
    created_at = models.DateTimeField(auto_now_add=True)
    feedburner = models.URLField(null=True, blank=True)
    feedburner_location = models.URLField(null=True, blank=True)
    handle = models.CharField(max_length=255)
    tags = models.CharField(max_length=255)
    template_suffix = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    admin_graphql_api_id = models.CharField(max_length=255)

    def __str__(self):
        return self.title