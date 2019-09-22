from flask import Flask, make_response, request, jsonify
from flask_api import status,mediatypes
import pandas as pd
import os
from discovery.discovery_service import DiscoveryService
from data.data_manager import DataManager

_METHOD_GET = 'GET'
_METHOD_POST = 'POST'

_DATASET_PATH = "dataset_path"

data_manager = DataManager()

app = Flask(__name__)

@app.route('/')
def index():
  return 'Server Works!', status.HTTP_200_OK

@app.route('/dataset', methods = [_METHOD_POST, _METHOD_GET])
def load_dataset():
  if request.method == _METHOD_GET:
    dataset_rows = data_manager.get_dataset_rows(as_csv=True)
    response = make_response(dataset_rows)
    response.headers["Content-type"] = "text/csv"
    return response, 200
  elif request.method == _METHOD_POST:
    dataset_path = request.form.get(_DATASET_PATH)
    data_manager.load_dataset(dataset_path)
    return 'Dataset loaded.', 201


with app.app_context():
  _discovery_service = DiscoveryService(debug=True)
  _discovery_service.start()

if __name__ == '__main__':
  app.run(port=8080)