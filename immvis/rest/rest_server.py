from flask import Flask, make_response, request, jsonify
from flask_api import status,mediatypes
import pandas as pd

_METHOD_GET = 'GET'
_METHOD_POST = 'POST'

app = Flask(__name__)

@app.route('/')
def index():
  return 'Server Works!', status.HTTP_200_OK

