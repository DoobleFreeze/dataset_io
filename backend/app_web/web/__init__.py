import logging
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from typing import Union

from .database.db_operator import DBOperator
from .handlers.main_controller import MainController
from .handlers.session_keeper import SessionKeeper

logger: Union[logging.Logger, None] = None
db_operator: Union[DBOperator, None] = None
main_control: Union[MainController, None] = None
keeper: Union[SessionKeeper, None] = None


def create_api(flask_log: bool,
               logging_cgf_path: str,
               db_host: str,
               db_port: int,
               db_login: str,
               db_password: str,
               db_name: str
               ) -> Flask:
    global logger, db_operator, main_control, keeper

    app = Flask(__name__)
    CORS(app)

    # Инициализация логирования
    from .initialization_logger import get_logger
    logger = get_logger(
        logging_cfg_path=logging_cgf_path,
        flask_log=flask_log,
        flask_app=app,
    )

    # Инициализация Базы данных
    db_operator = DBOperator(
        logger=logger,
        db_host=db_host,
        db_port=db_port,
        db_login=db_login,
        db_password=db_password,
        db_name=db_name
    )

    main_control = MainController(
        logger=logger
    )

    keeper = SessionKeeper(
        logger=logger
    )

    # from . import endpoint_api_controllers as api_control
    from .handlers.global_values import JSON_ERROR_NOT_FOUND
    from . import endpoint_api_controllers as api_control

    # # Подключение endpoint`ов
    app.register_blueprint(api_control.module)

    @app.errorhandler(404)
    def not_found(_error):
        """
        Обработчик 404 ошибки

        При возникновении ситуации, когда пользователь обращается по URL к
        которому не существует обработчика, сработает данный обработчик. В
        ответ он вернёт JSON с ошибкой (HTTP код 404). JSON формируется из
        шаблонов файла `global_values`.

        Arguments:
            _error: Обязательный параметр декоратора.

        Returns:
            Response - JSON с ошибкой и 404 HTTP код.
        """
        return make_response(jsonify(JSON_ERROR_NOT_FOUND), JSON_ERROR_NOT_FOUND['response_code'])

    return app
