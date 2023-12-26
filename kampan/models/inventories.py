# Inventories --> คลังสินค้า, สินค้าคงเหลือ

from email.policy import default
import mongoengine as me
import datetime


class RegistrationItem(me.Document):
    meta = {"collection": "registration_items"}

    bill = me.FileField()
    status = me.StringField(default="active")
    receipt_id = me.StringField(required=True, max_length=255)
    description = me.StringField()
    supplier = me.ReferenceField("Supplier", dbref=True)

    user = me.ReferenceField("User", dbref=True)
    created_date = me.DateTimeField(required=True, default=datetime.datetime.now)

    def get_item_in_bill(self):
        inventories = Inventory.objects(registration=self, status="active")
        if inventories:
            return [inventory.item.id for inventory in inventories]


class Inventory(me.Document):
    # อุปกรณ์
    meta = {"collection": "inventories"}
    status = me.StringField(default="active")

    registration = me.ReferenceField("RegistrationItem", dbref=True)
    warehouse = me.ReferenceField("Warehouse", dbref=True)
    item = me.ReferenceField("Item", dbref=True)
    # bill = me.FileField()

    quantity = me.IntField(required=True, min_value=1, default=1)
    remain = me.IntField(required=True, default=0)
    price = me.DecimalField(required=True, default=0)

    registeration_date = me.DateTimeField(
        required=True, default=datetime.datetime.now()
    )
    expiration_date = me.DateTimeField()
    position = me.ReferenceField("ItemPosition", dbref=True)

    # notification_status = me.BooleanField(default=True)
    user = me.ReferenceField("User", dbref=True)

    def get_checkout_items(self):
        return CheckoutItem.objects(checkout_from=self, status="active")

    def get_bill_file_name(self):
        if self.registration.bill:
            return self.registration.bill.filename
        else:
            return "ไม่พบบิล"


class OrderItem(me.Document):
    # เบิกอุปกรณ์
    meta = {"collection": "order_items"}
    status = me.StringField(default="active")

    approval_status = me.StringField(default="pending")
    description = me.StringField()
    user = me.ReferenceField("User", dbref=True)
    created_date = me.DateTimeField(required=True, default=datetime.datetime.now)
    approved_date = me.DateTimeField(required=True, default=datetime.datetime.now)

    def get_all_price(self):
        return sum(
            [
                item_checkout.price * item_checkout.quantity
                for item_checkout in CheckoutItem.objects(
                    status="active",
                    order=self,
                )
            ]
        )


class CheckoutItem(me.Document):
    # รายการนำเข้าอุปกรณ์ออก
    meta = {"collection": "checkout_items"}

    user = me.ReferenceField("User", dbref=True)
    status = me.StringField(default="active")

    order = me.ReferenceField("OrderItem", dbref=True)
    checkout_from = me.ReferenceField("Inventory", dbref=True)
    warehouse = me.ReferenceField("Warehouse", dbref=True)
    item = me.ReferenceField("Item", dbref=True)
    approval_status = me.StringField(default="pending")

    quantity = me.IntField(required=True, min_value=1, default=1)
    price = me.DecimalField(default=0.0)
    message = me.StringField()
    approved_date = me.DateTimeField()
    checkout_date = me.DateTimeField(required=True, default=datetime.datetime.now())


class LostBreakItem(me.Document):
    # ไอเทมที่ชำรุด หรือ เสียหาย
    mete = {"collection": "lost_break_items"}
    status = me.StringField(default="active")

    user = me.ReferenceField("User", dbref=True)
    item = me.ReferenceField("Item", dbref=True)

    lost_from = me.ReferenceField("Inventory", dbref=True)
    warehouse = me.ReferenceField("Warehouse", dbref=True)
    description = me.StringField(max_length=255)
    quantity = me.IntField(required=True, min_value=1, default=1)
    created_date = me.DateTimeField(required=True, default=datetime.datetime.now)


class Approve_orders(me.Document):
    # อนุมัติเบิก
    meta = {"collection": "approve_orders"}
    status = me.StringField(default="active")

    reated_date = me.DateTimeField(required=True, default=datetime.datetime.now)
