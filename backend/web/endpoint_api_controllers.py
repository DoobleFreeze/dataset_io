import os.path
import traceback
import random
from flask import Blueprint, request, make_response, jsonify, send_from_directory

from . import logger, db_operator, main_control, keeper
from .handlers.global_values import *

symbols = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c',
           'v', 'b', 'n', 'm', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K',
           'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

module = Blueprint(name='api_page', import_name=__name__, url_prefix='/api')


def generate_code(len_key=16):
    key = ''
    for _ in range(len_key):
        key += random.choice(symbols)
    return key


@module.route('/registration', methods=['POST'])
def registration():
    try:
        coming_json = request.json
        if coming_json['password'] != coming_json['second_password']:
            response_json = JSON_ERROR_BAD_REQUEST.copy()
            response_json['detail'] = "Пароли не совпадают!"
            return make_response(jsonify(response_json), response_json['response_code'])

        is_new_user = db_operator.registration(login=coming_json['login'],
                                               email=coming_json['email'],
                                               password=coming_json['password'])
        if not is_new_user:
            response_json = JSON_ERROR_BAD_REQUEST.copy()
            response_json['detail'] = "Почта занята!"
            return make_response(jsonify(response_json), response_json['response_code'])

        return make_response(jsonify(JSON_SUCCESS_POST), JSON_SUCCESS_POST['response_code'])
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC='api/registration method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/auth', methods=['POST'])
def auth():
    try:
        coming_json = request.json
        is_success, user_id = db_operator.auth(email=coming_json['email'],
                                               password=coming_json['password'])
        if not is_success:
            response_json = JSON_ERROR_BAD_REQUEST.copy()
            response_json['detail'] = "Неверно указан логин или пароль!"
            return make_response(jsonify(response_json), response_json['response_code'])

        user_session = keeper.add_session(user_id=user_id)
        response_json = JSON_SUCCESS_POST.copy()
        response_json['session'] = user_session

        return make_response(jsonify(response_json), response_json['response_code'])
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC='api/auth method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/logout', methods=['POST'])
def logout():
    try:
        coming_json = request.json

        keeper.delete_session(user_session=coming_json['user_session'])

        return make_response(jsonify(JSON_SUCCESS_POST), JSON_SUCCESS_POST['response_code'])
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC='api/logout method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/check/<string:user_session>', methods=['GET'])
def check(user_session):
    try:
        user_id = keeper.check_session(user_session=user_session)
        if user_id is None:
            response_json = JSON_ERROR_BAD_REQUEST.copy()
            response_json['detail'] = "Пользователь не активен"
            return make_response(jsonify(response_json), response_json['response_code'])

        response_json = JSON_SUCCESS_GET.copy()
        response_json['data'] = user_id
        return make_response(jsonify(response_json), response_json['response_code'])
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC='api/check/<user_session> method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/get_user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user_info = db_operator.get_user(user_id)
        response_json = JSON_SUCCESS_GET.copy()
        response_json['data'] = user_info
        return make_response(jsonify(response_json), response_json['response_code'])
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC='api/check/<user_session> method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/get_dashboard', methods=['GET'])
def get_dashboard():
    try:
        dashboard_info = db_operator.get_dashboard()
        response_json = JSON_SUCCESS_GET.copy()
        response_json['data'] = dashboard_info
        return make_response(jsonify(response_json), response_json['response_code'])
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC='api/check/<user_session> method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/get_user_dashboard/<int:user_id>', methods=['GET'])
def get_user_dashboard(user_id):
    try:
        dashboard_info = db_operator.get_user_dashboard(user_id)
        response_json = JSON_SUCCESS_GET.copy()
        response_json['data'] = dashboard_info
        return make_response(jsonify(response_json), response_json['response_code'])
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC='api/check/<user_session> method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/get_datasets', methods=['GET'])
def get_datasets():
    try:
        datasets_info = db_operator.get_datasets()
        response_json = JSON_SUCCESS_GET.copy()
        response_json['data'] = datasets_info
        return make_response(jsonify(response_json), response_json['response_code'])
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC='api/check/<user_session> method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/delete_dataset/<int:dataset_id>', methods=['GET'])
def delete_dataset(dataset_id):
    try:
        db_operator.delete_dataset(dataset_id)
        return make_response(jsonify(JSON_SUCCESS_DELETE), JSON_SUCCESS_DELETE['response_code'])
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC='api/check/<user_session> method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/get_dataset/<int:dataset_id>/<int:user_id>', methods=['GET'])
def get_dataset(dataset_id, user_id):
    try:
        file_path = db_operator.get_path_dataset(dataset_id, user_id)
        logger.debug(f"{os.getcwd()}")
        logger.debug(f"{round((os.path.getsize(f'./web/datasets/{file_path}') / 1024) / 1024, 2)}")
        return send_from_directory(f"datasets", file_path)
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC='api/check/<user_session> method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/add_dataset/<int:user_id>/<string:name_file>', methods=['POST'])
def add_dataset(user_id, name_file):
    try:
        video = request.files['dataset'].read()
        new_name = generate_code(len_key=64)
        with open(f'./web/datasets/{new_name}.zip', "wb") as f:
            f.write(video)
        count_memory = round((os.path.getsize(f'./web/datasets/{new_name}') / 1024) / 1024, 2)
        db_operator.add_dataset(user_id, name_file, new_name, count_memory)
        return make_response(jsonify(JSON_SUCCESS_POST), JSON_SUCCESS_POST['response_code'])
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC='api/logout method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/get_profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    try:
        datasets_info = db_operator.get_profile(user_id)
        response_json = JSON_SUCCESS_GET.copy()
        response_json['data'] = datasets_info
        response = jsonify(response_json)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return make_response(response, response_json['response_code'])
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC='api/logout method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/update_user/<int:user_id>', methods=['POST'])
def update_user(user_id):
    try:
        coming_json = request.json

        db_operator.update_user(user_id,
                                coming_json['login'],
                                coming_json['password'],
                                coming_json['image_path'],
                                )

        return make_response(jsonify(JSON_SUCCESS_POST), JSON_SUCCESS_POST['response_code'])
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC='api/registration method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))
