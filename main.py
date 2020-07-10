from flask import (Flask, 
                   make_response, 
                   abort, 
                   redirect, 
                   render_template, )
from flask_script import Manager

app = Flask(__name__)
manager = Manager(app)

@app.route("/")
def index():
    return render_template("index.html")


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
    return f"<h1> Hello {reverse} </h1>"


if __name__ == "__main__":
    manager.run()