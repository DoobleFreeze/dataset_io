from .db_session import global_init, create_session
from .tables.users import Users
from .tables.datasets import Datasets
from .tables.user_history import UserHistory


class DBOperator:
    def __init__(self, db_host, db_port, db_login, db_password, db_name, logger):
        global_init(
            logger=logger,
            db_host=db_host,
            db_port=db_port,
            db_login=db_login,
            db_password=db_password,
            db_name=db_name
        )
        self.logger = logger
