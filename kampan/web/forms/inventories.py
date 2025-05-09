from dataclasses import field
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import fields, validators, widgets
from .fields import TagListField, TextListField

from flask_mongoengine.wtf import model_form
from kampan import models

BaseInventoryForm = model_form(
    models.Inventory,
    FlaskForm,
    exclude=[
        "created_date",
        "expiration_date",
        "created_by",
        "remain",
        "status",
        "quantity",
        "position",
        "organization",
    ],
    field_args={
        # "item": {
        #     "label": "วัสดุ",
        #     "label_modifier": lambda i: f"{i.barcode_id} ({i.name})",
        # },
        # "position": {
        #     "label": "ตำแหน่ง",
        #     "label_modifier": lambda p: f"{p.description} ({p.warehouse.name})",
        # },
        # "warehouse": {"label": "คลังวัสดุ", "label_modifier": lambda w: w.name},
        "set_": {"label": "จำนวนหน่วยใหญ่"},
        "price": {"label": "ราคา (หน่วยใหญ่ละ)"},
    },
)


class InventoryForm(BaseInventoryForm):
    warehouse = fields.SelectField(
        "คลังวัสดุ",
    )
    item = fields.SelectField("วัสดุ", choices=[("", "Item")])
    calendar_select = fields.DateTimeField("วันที่เริ่มต้น")
    calendar_end = fields.DateTimeField("วันที่สุดท้าย")
    calendar_month_year = fields.DateTimeField("กรุณาเลือกเดือนและปี", format="%Y-%m")
    calendar_year = fields.DateTimeField("กรุณาเลือกปี", format="%Y")


class UploadInventoryFileForm(FlaskForm):
    upload_file = fields.FileField(
        "*** อัปโหลดเฉพาะไฟล์ที่เป็นไฟล์ .xlsx เท่านั้น ***",
        validators=[FileAllowed(["xlsx"], "xlsx only")],
    )


class SearchStartEndDateForm(FlaskForm):
    start_date = fields.DateField(
        "วันที่เริ่มต้น",
        validators=[validators.Optional()],
    )
    end_date = fields.DateField(
        "วันที่สุดท้าย",
        validators=[validators.Optional()],
    )
    item = fields.SelectField(
        "วัสดุ", validate_choice=False, validators=None, choices=[("", "ไม่เลือก")]
    )
    categories = fields.SelectField("หมวดหมู่", validate_choice=False)


class SearchMonthYearForm(FlaskForm):
    month_year = fields.MonthField(
        "เดือนที่เลือก", format="%m/%Y", widget=widgets.TextInput()
    )


class SearchYearForm(FlaskForm):
    year = fields.IntegerField("ปีที่เลือก")
