from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from kampan.web import forms
from kampan import models
import mongoengine as me

module = Blueprint("item_registers", __name__, url_prefix="/item_registers")


@module.route("/")
@login_required
def index():
    item_registers = models.RegistrationItem.objects()
    return render_template(
        "/item_registers/index.html",
        item_registers=item_registers,
    )


@module.route("/register", methods=["GET", "POST"], defaults=dict(item_register_id=None))
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

    form.populate_obj(item_register)
    item_register.save()

    return redirect(url_for("item_registers.index"))

@module.route("/<item_register_id>/delete")
@login_required
def delete(item_register_id):
    item_register = models.RegistrationItem.objects().get(id=item_register_id)
    item_register.delete()

    return redirect(url_for("item_registers.index"))