from flask import (Flask, 
                   make_response, 
                   abort, 
                   redirect, 
                   render_template, 
                   url_for, 
                   flash, 
                   session, )
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form

from wtforms import StringField, SubmitField
from wtforms.validators import Required

from datetime import datetime
import os


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", default="some secret key here")


###### Init side apps #######

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

########## Forms ############

class NameForm(Form):
    name = StringField("What is your name", validators=[Required()])
    submit = SubmitField("Submit")

########## Routes ###########

@app.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get("name")
        if old_name is not None and old_name != form.name.data:
            flash("You have changed your name!")
        session["name"], form.name.data = form.name.data, ""
        return redirect(url_for("index"))
    return render_template("index.html", form=form, 
                           name=session.get("name"),
                           current_time=datetime.utcnow())


@app.route("/<word>")
def reverse_word(word):
    if word == "smth":
        abort(404)
    elif word == "something":
        return redirect("braza")
    else:
        pass
    i = 1
    reverse = ""
    while len(word) >= i:
        reverse += word[-i]
        i += 1
    return render_template("user.html", name=word)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    manager.run()