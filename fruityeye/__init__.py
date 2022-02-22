from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__)

from fruityeye import fruity_backend
