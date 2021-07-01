from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.testing.config import db
from werkzeug.utils import secure_filename
from flask.wrappers import Response
from PIL import Image
import io
import base64

# Assuming UTF-8 encoding, change to something else if you need to
base64.b64encode("password".encode("utf-8"))

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///imgfolder.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Img(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    db.create_all()
    db.session.commit()


@app.route('/')
def hello_world():
    return render_template("base.html")


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        pic = request.files["pic"]
        if not pic:
            return 'No pic uploaded!', 400

        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            return 'Bad upload!', 400

        img = Img(img=pic.read(), name=filename, mimetype=mimetype)
        db.session.add(img)
        db.session.commit()
    return render_template("addpictures.html")


@app.route("/display/<int:id>")
def display(id):
    image = Img.query.filter_by(sno=id).first()
    if not image:
        return "Image Not Found", 404
    img = image.img
    img_encoded = base64.encodebytes(img)
    allpic = Img.query.all()
    return render_template("displaypictures.html", img_data=img_encoded.decode('utf-8'), img_name=image.name, id=image.sno,allpic=allpic)


@app.route("/display")
def view():
    number=1
    img=Img.query.filter_by(sno=number).first()
    name=img.name
    mimetype=img.mimetype
    allpic = Img.query.all()
    return render_template("display.html",name=name,mimetype=mimetype,allpic=allpic)



@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/privacy")
def privacy():
    return render_template("privacypolicy.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
