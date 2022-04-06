# importing required python libraries
import os
from flask import Flask, request, render_template, send_from_directory,Response
from fruityeye import app
from fruityeye.rotten_image_classifier import prediction_func
from fruityeye.fruit_classifier import prediction_func2
from fruityeye.camera import Video
from fruityeye.audio_out import voice_out

# import tensorflow as tf
# gpus = tf.config.list_physical_devices('GPU')
# if gpus:
#     try:
#         # Currently, memory growth needs to be the same across GPUs
#         for gpu in gpus:
#             tf.config.experimental.set_memory_growth(gpu, True)
#         logical_gpus = tf.config.experimental.list_logical_devices('GPU')
#         print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
#     except RuntimeError as e:
#         # Memory growth must be set before GPUs have been initialized
#         print(e)

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

        # Calling voice out function to give audio output
        voice_out_text = pred+" Detected"
        voice_out(voice_out_text)

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

# ------------------------------------------------------------------

@app.route("/fruit_cls")
def fruit_cls():
    print(APP_ROOT)
    return render_template("classify.html")

# route to show output result
@app.route("/fruit_img", methods=["POST"])
def fruit_img():
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
        pred, k = prediction_func2(filename)

    return render_template("out2.html", image_name=filename, text=pred, value=k)

# route to load image to page
@app.route('/fruit_img/<filename>')
def fruit_img_send(filename):
    return send_from_directory("images", filename)
# ------------------------------------------------------------------


@app.route('/real_time_condition')
def real_time_condition():
    return render_template('real_condition.html')

@app.route('/video')
def video():
    return Response(gen(Video()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def gen(camera):
    img_text = ''
    image_x, image_y = 500, 500
    while True:
        frame = camera.get_frame(img_text, image_x, image_y)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame +
               b'\r\n\r\n')