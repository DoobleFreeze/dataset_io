import sqlalchemy
import datetime
from sqlalchemy import orm

from ..db_session import SqlAlchemyBase


class UserHistory(SqlAlchemyBase):
    __tablename__ = 'user_history'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    dataset_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("datasets.id"))
    type_operation = sqlalchemy.Column(sqlalchemy.Text)
    date_operation = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    users = orm.relationship('Users', backref="user_history")
    datasets = orm.relationship('Datasets', backref="user_history")
