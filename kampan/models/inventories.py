import mongoengine as me
import datetime


class RegistrationItem(me.Document):
    meta = {"collection": "registration_items"}
    receipt_id = me.StringField(required=True, max_length=255)
    description = me.StringField()
    supplier = me.ReferenceField("Supplier", dbref=True)
    user = me.ReferenceField("User", dbref=True)
    created_date = me.DateTimeField(required=True, default=datetime.datetime.now)


class Inventory(me.Document):
    meta = {"collection": "inventories"}

    registration = me.ReferenceField("RegistrationItem", dbref=True)
    warehouse = me.ReferenceField("Warehouse", dbref=True)
    item = me.ReferenceField("Item", dbref=True)

    quantity = me.IntField(required=True, default=0)
    remain = me.IntField(required=True, default=0)
    price = me.FloatField(required=True, default=0)

    registeration_date = me.DateTimeField(
        required=True, default=datetime.datetime.now()
    )
    expiration_date = me.DateTimeField()
    position = me.ReferenceField("ItemPosition", dbref=True)

    user = me.ReferenceField("User", dbref=True)

    def get_checkout_items(self):
        return CheckoutItem.objects(checkout_from=self)


class OrderItem(me.Document):
    meta = {"collection": "order_items"}

    description = me.StringField()
    user = me.ReferenceField("User", dbref=True)
    created_date = me.DateTimeField(required=True, default=datetime.datetime.now)


class CheckoutItem(me.Document):
    meta = {"collection": "checkout_items"}

    order = me.ReferenceField("OrderItem", dbref=True)
    checkout_from = me.ReferenceField("Inventory", dbref=True)
    warehouse = me.ReferenceField("Warehouse", dbref=True)
    item = me.ReferenceField("Item", dbref=True)

    quantity = me.FloatField(required=True)
    price = me.FloatField()
    message = me.StringField()

    checkout_date = me.DateTimeField(required=True, default=datetime.datetime.now())
