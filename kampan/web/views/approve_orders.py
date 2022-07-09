from pyexpat import model
from flask import Blueprint, render_template, redirect, url_for, request, send_file
from flask_login import login_required, current_user
from kampan.web import forms
from kampan import models

module = Blueprint("approve_orders", __name__, url_prefix="/approve_orders")


@module.route("/")
@login_required
def index():
    orders = models.OrderItem.objects()
    
    return render_template(
        "/approve_orders/index.html",
        orders=orders,
    )

@module.route("<checkout_item_id>", methods=["GET", "POST"])
def approve(checkout_item_id):
    checkout_item = models.CheckoutItem.objects.get(id=checkout_item_id)
    form = forms.item_orders.OrderItemForm(obj=checkout_item)
    order_id = request.args.get("order_id")
    order = models.OrderItem.objects.get(id=order_id)
    checkout_items = models.CheckoutItem.objects()
    
    form.populate_obj(checkout_item)

    checkout_item.status = "approved"
    checkout_item.save()

    for checkout in checkout_items:
        if checkout.order.id == order.id:
            if checkout.status == "pending":
                return redirect(url_for("item_checkouts.bill_checkout"))

    form.populate_obj(order)
    order.status = "approved"
    order.save()
    
    return redirect(url_for("approve_orders.index"))
