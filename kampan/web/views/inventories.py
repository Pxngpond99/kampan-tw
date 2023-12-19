from calendar import calendar
from pyexpat import model
from tabnanny import check
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    send_file,
    abort,
)
from flask_login import login_required, current_user
from kampan.web import forms
from kampan import models

module = Blueprint("inventories", __name__, url_prefix="/inventories")


@module.route("/", methods=["GET", "POST"])
@login_required
def index():
    form = forms.inventories.SearchStartEndDateForm()
    inventories = models.Inventory.objects(status="active")

    if form.start_date.data == None and form.end_date.data != None:
        inventories = inventories.filter(
            registeration_date__lte=form.end_date.data,
        )

    elif form.start_date.data and form.end_date.data == None:
        inventories = inventories.filter(
            registeration_date__gte=form.start_date.data,
        )

    elif form.start_date.data != None and form.end_date.data != None:
        inventories = inventories.filter(
            registeration_date__gte=form.start_date.data,
            registeration_date__lte=form.end_date.data,
        )
    # print(form.errors)
    return render_template(
        "/inventories/index.html",
        inventories=inventories,
        form=form,
    )


@module.route("/register", methods=["GET", "POST"])
@login_required
def register():
    form = forms.inventories.InventoryForm()
    item_register_id = request.args.get("item_register_id")
    item_register = models.RegistrationItem.objects.get(id=item_register_id)

    if not form.validate_on_submit():
        print(form.errors)
        return render_template(
            "/inventories/register.html",
            form=form,
            item_register=item_register,
        )

    inventory = models.Inventory()
    form.populate_obj(inventory)

    # if form.bill_file.data:
    #     if inventory.bill:
    #         inventory.bill.replace(
    #             form.bill_file.data,
    #             filename=form.bill_file.data.filename,
    #             content_type=form.bill_file.data.content_type,
    #         )
    #     else:
    #         inventory.bill.put(
    #             form.bill_file.data,
    #             filename=form.bill_file.data.filename,
    #             content_type=form.bill_file.data.content_type,
    #         )

    inventory.user = current_user._get_current_object()
    inventory.notification_status = True
    inventory.registration = item_register
    inventory.remain = inventory.quantity
    inventory.save()

    return redirect(url_for("item_registers.index"))


@module.route("/<inventory_id>/edit", methods=["GET", "POST"])
@login_required
def edit(inventory_id):
    inventory = models.Inventory.objects().get(id=inventory_id)
    form = forms.inventories.InventoryForm(obj=inventory)
    item_register = inventory.registration

    if not form.validate_on_submit():
        return render_template(
            "/inventories/register.html",
            item_register=item_register,
            form=form,
        )

    form.populate_obj(inventory)
    # if form.bill_file.data:
    #     if inventory.bill:
    #         inventory.bill.replace(
    #             form.bill_file.data,
    #             filename=form.bill_file.data.filename,
    #             content_type=form.bill_file.data.content_type,
    #         )
    #     else:
    #         inventory.bill.put(
    #             form.bill_file.data,
    #             filename=form.bill_file.data.filename,
    #             content_type=form.bill_file.data.content_type,
    #         )

    inventory.user = current_user._get_current_object()
    inventory.registration = item_register
    inventory.remain = inventory.quantity
    inventory.save()

    return redirect(
        url_for("inventories.bill_item", item_register_id=inventory.registration.id)
    )


@module.route("/<inventory_id>/delete")
@login_required
def delete(inventory_id):
    inventory = models.Inventory.objects().get(id=inventory_id)
    inventory.status = "disactive"
    inventory.save()

    return redirect(
        url_for("inventories.bill_item", item_register_id=inventory.registration.id)
    )


@module.route("item_register/<item_register_id>/all-item", methods=["GET", "POST"])
@login_required
def bill_item(item_register_id):
    item_register = models.RegistrationItem.objects.get(id=item_register_id)
    inventories = models.Inventory.objects(registration=item_register)

    return render_template(
        "/inventories/bill-item.html",
        inventories=inventories,
        item_register=item_register,
    )


@module.route("/<inventory_id>/file")
def bill(inventory_id):
    inventory = models.Inventory.objects.get(id=inventory_id)

    if not inventory:
        return abort(404)

    response = send_file(
        inventory.bill,
        download_name=inventory.bill.filename,
        mimetype=inventory.bill.content_type,
    )
    return response
