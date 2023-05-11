import traceback
from flask import Blueprint, request, make_response, jsonify

from . import logger, db_operator, main_control, keeper
from .handlers.global_values import *

module = Blueprint(name='api_page', import_name=__name__, url_prefix='/api')


@module.route('/registration', methods=['POST'])
def registration():
    try:
        coming_json = request.json

        return make_response(jsonify(JSON_SUCCESS_POST), JSON_SUCCESS_POST['response_code'])
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC='api/registration method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))
