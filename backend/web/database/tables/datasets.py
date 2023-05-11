import sqlalchemy
import datetime
from sqlalchemy import orm

from ..db_session import SqlAlchemyBase


class Datasets(SqlAlchemyBase):
    __tablename__ = 'datasets'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.Text)
    file_path = sqlalchemy.Column(sqlalchemy.Text)
    memory_used = sqlalchemy.Column(sqlalchemy.Float)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    date_load = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    is_deleted = sqlalchemy.Column(sqlalchemy.Boolean)

    users = orm.relationship('Users', backref="datasets")
