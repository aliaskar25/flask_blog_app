from flask import Blueprint
from ..models import Permission


main = Blueprint("main", __name__)

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission) # Set permission context


from . import views, errors # these modules should be imported after init Blueprint