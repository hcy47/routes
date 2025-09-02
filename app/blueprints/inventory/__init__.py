from flask import Blueprint

inventorys_bp =  Blueprint('inventorys_bp', __name__)

from . import routes