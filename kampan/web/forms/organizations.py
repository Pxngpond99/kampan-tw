from flask_mongoengine.wtf import model_form
from flask_wtf import FlaskForm, file
from wtforms import fields, widgets, validators

from kampan import models

BaseOrganizationForm = model_form(
    models.Organization,
    FlaskForm,
    exclude=[
        "created_date",
        "updated_date",
        "created_by",
        "last_updated_by",
        "status",
    ],
    field_args={
        "name": {"label": "Name"},
        "description": {"label": "Desctiption"},
        "authenticity_text": {"label": "Authenticity Text"},
    },
)


class OrganizationForm(BaseOrganizationForm):
    pass


BaseLogoForm = model_form(
    models.Logo,
    FlaskForm,
    only=["logo_name"],
    field_args={
        "logo_name": {"label": "Logo Name"},
    },
)


class LogoForm(BaseLogoForm):
    uploaded_logo_file = file.FileField(
        "Logo File",
        validators=[
            file.FileAllowed(["png", "jpg"], "รับเฉพาะไฟล์ png เเละ jpg เท่านั้น"),
        ],
    )


class OrganizationUserForm(FlaskForm):
    users = fields.SelectMultipleField("")


class OrganizationRoleSelectionForm(FlaskForm):
    role = fields.SelectField(choices=models.organizations.ORGANIZATION_ROLES)


class OrgnaizationAddMemberForm(FlaskForm):
    members = fields.SelectMultipleField("Select Members")
    role = fields.SelectField("Role", choices=models.organizations.ORGANIZATION_ROLES)


class AdminOrganizationEditForm(BaseOrganizationForm):
    pass


class SearchUserForm(FlaskForm):
    start_date = fields.DateField(
        "เริ่มเพิ่มเมื่อวันที่",
        format="%d/%m/%Y",
        widget=widgets.TextInput(),
        render_kw={"placeholder": "Date"},
    )
    end_date = fields.DateField(
        "จนถึงวันที่",
        format="%d/%m/%Y",
        widget=widgets.TextInput(),
        render_kw={"placeholder": "Date"},
    )
    role = fields.SelectField(
        "ตำแหน่ง",
        choices=[("", "Role")] + models.organizations.ORGANIZATION_ROLES,
        validate_choice=False,
        validators=None,
        render_kw={"placeholder": "role"},
    )
    user = fields.SelectField(
        "สมาชิก",
        choices=[("", "User")],
        validate_choice=False,
        validators=None,
        render_kw={"placeholder": "user"},
    )
