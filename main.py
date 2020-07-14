from flask import (Flask, 
                   make_response, 
                   abort, 
                   redirect, 
                   render_template, 
                   url_for, 
                   flash, 
                   session, )
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail, Message

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from datetime import datetime
import os
from threading import Thread


basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", default="some secret key here")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_SUBJECT"] = "eeee BOOY"
app.config["MAIL_SENDER"] = "prosto@chel.com"
app.config["ADMIN_MAIL"] = "aliaskar.isakov@yandex.ru"

###### Init side apps #######

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

########## Models ###########

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    users = db.relationship("User", backref="role", lazy="dynamic")
    
    def __repr__(self):
        return f"<Role {self.name}>"


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=True)

    def __repr__(self):
        return f"<User {self.username}>"

########## Forms ############

class NameForm(FlaskForm):
    name = StringField("What is your name", validators=[DataRequired()])
    submit = SubmitField("Submit")

########### Utils ###########

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(to, template, **kwargs):
    msg = Message(app.config["MAIL_SUBJECT"], 
                  sender=app.config["MAIL_SENDER"],
                  recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
    

########## Routes ###########

@app.route("/", methods=["GET", "POST"])
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
            if app.config["ADMIN_MAIL"]:
                send_mail(app.config["ADMIN_MAIL"], "mail/new_user", user=user)
        session["name"], form.name.data = form.name.data, ""
        return redirect(url_for("index"))
    return render_template("index.html", form=form, 
                           name=session.get("name"),
                           known=session.get("known", False),
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