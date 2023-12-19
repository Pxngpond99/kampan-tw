from calendar import calendar
from crypt import methods
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from kampan.web import forms
from kampan import models
import mongoengine as me

module = Blueprint("item_registers", __name__, url_prefix="/item_registers")


@module.route("/", methods=["GET", "POST"])
@login_required
def index():
    item_registers = models.RegistrationItem.objects(status="active")
    form = forms.inventories.SearchStartEndDateForm()

    if form.validate_on_submit():
        if form.start_date.data != None and form.end_date.data != None:
            print(form.errors)
            item_registers = item_registers.filter(
                created_date__gte=form.start_date.data,
                created_date__lte=form.end_date.data,
            )

    return render_template(
        "/item_registers/index.html",
        item_registers=item_registers,
        form=form,
    )


@module.route(
    "/register", methods=["GET", "POST"], defaults=dict(item_register_id=None)
)
@login_required
def register(item_register_id):
    form = forms.item_registers.ItemRegisterationForm()

    item_register = None
    if item_register_id:
        item_register = models.RegistrationItem.objects().get(id=item_register_id)
        form = forms.item_registers.ItemRegisterationForm(obj=item_register)

    if not form.validate_on_submit():
        return render_template(
            "/item_registers/register.html",
            form=form,
        )

    if not item_register:
        item_register = models.RegistrationItem()

    if form.bill_file.data:
        item_register.bill.put(
            form.bill_file.data,
            filename=form.bill_file.data.filename,
            content_type=form.bill_file.data.content_type,
        )

    form.populate_obj(item_register)
    item_register.user = current_user._get_current_object()
    item_register.save()

    return redirect(url_for("item_registers.index"))


@module.route("/<item_register_id>/edit", methods=["GET", "POST"])
@login_required
def edit(item_register_id):
    item_register = models.RegistrationItem.objects().get(id=item_register_id)
    form = forms.item_registers.ItemRegisterationForm(obj=item_register)

    if not form.validate_on_submit():
        return render_template(
            "/item_registers/register.html",
            form=form,
        )
    if form.bill_file.data:
        if item_register.bill:
            item_register.bill.replace(
                form.bill_file.data,
                filename=form.bill_file.data.filename,
                content_type=form.bill_file.data.content_type,
            )
        else:
            item_register.bill.put(
                form.bill_file.data,
                filename=form.bill_file.data.filename,
                content_type=form.bill_file.data.content_type,
            )
    form.populate_obj(item_register)
    item_register.save()

    return redirect(url_for("item_registers.index"))


@module.route("/<item_register_id>/delete")
@login_required
def delete(item_register_id):
    item_register = models.RegistrationItem.objects().get(id=item_register_id)
    item_register.delete()

    return redirect(url_for("item_registers.index"))
