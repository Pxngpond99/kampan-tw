from flask import Blueprint, render_template ,redirect, url_for
from flask_login import login_required, current_user
from kampan.web import forms
from kampan import models
import mongoengine as me

import datetime

module = Blueprint('dashboard', __name__, url_prefix='/dashboard')
subviews = []


def index_admin():
    
    now = datetime.datetime.now()
    return render_template('/dashboard/index-admin.html',
                           now=datetime.datetime.now(),
                           available_classes=[])


def index_user():
    return render_template('/dashboard/index.html')


@module.route('/')
@login_required
def index():
    user = current_user._get_current_object()
    if 'admin' in user.roles:
        return index_admin()
    
    return index_user()
