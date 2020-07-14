from flask import (render_template, 
                   session, 
                   redirect, 
                   url_for, 
                   current_app, )
from datetime import datetime

from . import main
from .forms import NameForm

from .. import db # import db var from main init
from ..models import User
from ..email import send_email


@main.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user:
            session["known"] = True
        else:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session["known"] = False
            send_email(current_app.config["ADMIN_MAIL"], "mail/new_user", user=user)
        session["name"], form.name.data = form.name.data, ""
        return redirect(url_for(".index")) # dot here cause blueprint register path with dots main.index
    return render_template("index.html", form=form, 
                           name=session.get("name"),
                           known=session.get("known", False),
                           current_time=datetime.utcnow())
