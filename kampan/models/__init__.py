from flask_mongoengine import MongoEngine
from .users import User
from . import oauth2
from .oauth2 import OAuth2Token
from .items import ItemSize, Item, Location
from .orders import ItemRegisteration, ItemCheckout, Checkout
from .stocks import Supplier, Inventory

__all__ = ["User"]

db = MongoEngine()


def init_db(app):
    db.init_app(app)
