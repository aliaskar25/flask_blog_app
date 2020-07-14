from flask import Blueprint


main = Blueprint("main", __name__)


from . import views, errors # these modules should be imported after init Blueprint