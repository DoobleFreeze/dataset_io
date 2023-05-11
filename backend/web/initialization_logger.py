import logging.config
import logging
import yaml
from flask import Flask


def get_logger(logging_cfg_path: str, flask_log: bool, flask_app: Flask = None) -> logging.Logger:
    if flask_log:
        flask_app.logger.disabled = True
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

    logger_api = logging.getLogger('api_logger')

    with open(logging_cfg_path) as config_fin:
        logging.config.dictConfig(yaml.safe_load(config_fin.read()))

    return logger_api
