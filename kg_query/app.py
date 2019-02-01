import logging.config

import os
from flask import Flask, Blueprint
import config
from api.api_1_0.restplus import api
from api.api_1_0.endpoints.kbqa import ns as v0_0_1_namespace


app = Flask(__name__)
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "logging.conf"))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


# app.config['SERVER_NAME'] = config.FLASK_SERVER_NAME
app.config['SWAGGER_UI_DOC_EXPANSION'] = config.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
app.config['RESTPLUS_VALIDATE'] = config.RESTPLUS_VALIDATE
app.config['RESTPLUS_MASK_SWAGGER'] = config.RESTPLUS_MASK_SWAGGER
app.config['ERROR_404_HELP'] = config.RESTPLUS_ERROR_404_HELP

blueprint = Blueprint("api", __name__, url_prefix="/api")
api.init_app(blueprint)
api.add_namespace(v0_0_1_namespace)
app.register_blueprint(blueprint)

log.info(">>>>> Starting development server at http://{}/api/ <<<<<".format(app.config["SERVER_NAME"]))
app.run()
