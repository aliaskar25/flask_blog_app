from flask import (Flask, 
                   make_response, 
                   abort, 
                   redirect, 
                   render_template, )
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment

from datetime import datetime

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route("/")
def index():
    return render_template("index.html", current_time=datetime.utcnow())


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