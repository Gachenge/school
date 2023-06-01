#!/usr/bin/python3

from flask import Flask
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
from flask import jsonify
from flask import make_response

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] =True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def cloes(err):
    storage.close()

@app.errorhandler(404)
def page_not_found(err):
    return make_response(jsonify({"error": "Not Found"}))


if __name__ =="__main__":
    app.run(host='0.0.0.0', port='5000', threaded=True)
