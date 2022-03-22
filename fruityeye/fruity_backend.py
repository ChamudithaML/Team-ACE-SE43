# importing required python libraries
import os
from flask import Flask, request, render_template, send_from_directory
from fruityeye import app
from fruityeye.rotten_image_classifier import prediction_func

# route to home page
@app.route('/home')
@app.route('/')
def home_page():
    return render_template('home.html')

# to get the path of directory
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# route to condition checking page
@app.route("/rotten")
def condition():
    print(APP_ROOT)
    return render_template("condition.html")

# route to show output result
@app.route("/rot_image", methods=["POST"])
def rot_image():
    # creating path to save image
    target = os.path.join(APP_ROOT, 'images/')

    # creating directory if its not there
    if not os.path.isdir(target):
        os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))

    # getting the file from html form
    for im in request.files.getlist("file"):
        # getting the file name
        filename = im.filename

        # joining path and file name to variable
        destination = "/".join([target, filename])

        # saving file in destination
        im.save(destination)

        # calling the ML model function to get the prediction
        pred = prediction_func(filename)

    return render_template("out1.html", image_name=filename, text=pred)

# route to load image to page
@app.route('/rot_image/<filename>')
def rot_fresh_img(filename):
    return send_from_directory("images", filename)

# route to login page
@app.route('/login')
def login_page():
    return render_template('login.html')

# route to image gallery page
@app.route('/imageGallery')
def imageGallery_page():
    return render_template('imageGallery.html')
