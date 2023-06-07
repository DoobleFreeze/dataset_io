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

    def registration(self, login, email, password) -> bool:
        session = create_session()
        some_user = session.query(Users).filter(Users.email == email).first()
        if some_user is not None:
            return False

        new_user = Users(
            login=login,
            email=email,
            password=password,
        )
        session.add(new_user)
        session.commit()

        self.logger.debug("New user in DB")
        return True

    def auth(self, email, password):
        session = create_session()
        some_user = session.query(Users).filter(Users.email == email, Users.password == password).first()
        if some_user is not None:
            self.logger.debug("Success auth")
            return True, some_user.id
        return False, None

    def get_user(self, user_id):
        session = create_session()
        some_user = session.query(Users).filter(Users.id == user_id).first()
        if some_user:
            response_json = {"user": {
                "login": some_user.login,
                "email": some_user.email,
                "image_path": some_user.image_path
            }}
        else:
            response_json = {"user": {}}
        self.logger.debug("Get user")
        return response_json

    def get_dashboard(self):
        session = create_session()
        list_datasets = session.query(Datasets).filter(Datasets.is_deleted == False).all()
        list_users = session.query(Users).all()
        list_history = session.query(UserHistory).filter(UserHistory.type_operation == "Загрузил").all()
        count_memory = 0
        us_to_ds = {}
        for ds in list_datasets:
            if ds.user_id not in us_to_ds:
                us_to_ds[ds.user_id] = {
                    "memory": 0,
                    "count": 0
                }
            count_memory += ds.memory_used
            us_to_ds[ds.user_id]["memory"] += ds.memory_used
            us_to_ds[ds.user_id]["count"] += 1

        lst_date = list_history[-1].date_operation.strftime("%m")
        if lst_date == "01":
            labels = ["Ноябрь", "Декабрь", "Январь"]
            lst_dates = ['11', '12', lst_date]
        elif lst_date == "02":
            labels = ["Декабрь", "Январь", "Февраль"]
            lst_dates = ['12', '01', lst_date]
        elif lst_date == "03":
            labels = ["Январь", "Февраль", "Март"]
            lst_dates = ['01', '02', lst_date]
        elif lst_date == "04":
            labels = ["Февраль", "Март", "Апрель"]
            lst_dates = ['02', '03', lst_date]
        elif lst_date == "05":
            labels = ["Март", "Апрель", "Май"]
            lst_dates = ['03', '04', lst_date]
        elif lst_date == "06":
            labels = ["Апрель", "Май", "Июнь"]
            lst_dates = ['04', '05', lst_date]
        elif lst_date == "07":
            labels = ["Май", "Июнь", "Июль"]
            lst_dates = ['05', '06', lst_date]
        elif lst_date == "08":
            labels = ["Июнь", "Июль", "Август"]
            lst_dates = ['06', '07', lst_date]
        elif lst_date == "09":
            labels = ["Июль", "Август", "Сентябрь"]
            lst_dates = ['07', '08', lst_date]
        elif lst_date == "10":
            labels = ["Август", "Сентябрь", "Октябрь"]
            lst_dates = ['08', '09', lst_date]
        elif lst_date == "11":
            labels = ["Сентябрь", "Октябрь", "Ноябрь"]
            lst_dates = ['09', '10', lst_date]
        elif lst_date == "12":
            labels = ["Октябрь", "Ноябрь", "Декабрь"]
            lst_dates = ['10', '11', lst_date]
        else:
            labels = ["Нет", "Нет", "Нет"]
            lst_dates = ['0', '0', "0"]

        data_graf = [0, 0, 0]
        for hs in list_history:
            if hs.date_operation.strftime("%m") in lst_dates[0]:
                data_graf[0] += 1
            elif hs.date_operation.strftime("%m") in lst_dates[1]:
                data_graf[1] += 1
            elif hs.date_operation.strftime("%m") in lst_dates[2]:
                data_graf[2] += 1

        last_activity = []
        all_activity = session.query(UserHistory).all()
        for i in range(-1, -7, -1):
            user_info = session.query(Users).filter(Users.id == all_activity[i].user_id).first()
            ds_info = session.query(Datasets).filter(Datasets.id == all_activity[i].dataset_id).first()
            x = {
                "nickname": user_info.login,
                "image_path": user_info.image_path,
                "text_label": all_activity[i].type_operation + " датасет \"" + ds_info.name + "\"",
                "data_label": all_activity[i].date_operation.strftime("%d.%m.%Y")
            }
            last_activity.append(x)

        user_anal = []
        for us in list_users:
            x = {
                "nickname": us.login,
                "image_path": us.image_path,
                "memory": us_to_ds[us.id]["memory"] if us_to_ds.get(us.id, False) else 0,
                "count": us_to_ds[us.id]['count'] if us_to_ds.get(us.id, False) else 0
            }
            user_anal.append(x)

        response_json = {
            "panels": {
                "all_memory": count_memory,
                "count_ds": len(list_datasets),
                "count_download": len(list_history),
                "count_users": len(list_users),
            },
            "graf": {
                "labels": labels,
                "datasets": [
                    {
                        "label": 'Количество загруженных датасетов',
                        "data": data_graf,
                        "backgroundColor": ["#7000e1", "#FC8800", "#00B0E8"],
                        "borderWidth": 0
                    }
                ]
            },
            "last_activity": last_activity,
            "users_anal": user_anal
        }
        self.logger.debug(f"Get dashboard: {response_json}")
        return response_json

    def get_user_dashboard(self, user_id):
        session = create_session()
        list_datasets = session.query(Datasets).filter(Datasets.is_deleted == False,
                                                       Datasets.user_id == user_id).all()
        list_history = session.query(UserHistory).filter(UserHistory.type_operation == "Загрузил",
                                                         UserHistory.user_id == user_id).all()
        count_memory = 0
        for ds in list_datasets:
            count_memory += ds.memory_used

        lst_date = list_history[-1].date_operation.strftime("%m")
        if lst_date == "01":
            labels = ["Ноябрь", "Декабрь", "Январь"]
            lst_dates = ['11', '12', lst_date]
        elif lst_date == "02":
            labels = ["Декабрь", "Январь", "Февраль"]
            lst_dates = ['12', '01', lst_date]
        elif lst_date == "03":
            labels = ["Январь", "Февраль", "Март"]
            lst_dates = ['01', '02', lst_date]
        elif lst_date == "04":
            labels = ["Февраль", "Март", "Апрель"]
            lst_dates = ['02', '03', lst_date]
        elif lst_date == "05":
            labels = ["Март", "Апрель", "Май"]
            lst_dates = ['03', '04', lst_date]
        elif lst_date == "06":
            labels = ["Апрель", "Май", "Июнь"]
            lst_dates = ['04', '05', lst_date]
        elif lst_date == "07":
            labels = ["Май", "Июнь", "Июль"]
            lst_dates = ['05', '06', lst_date]
        elif lst_date == "08":
            labels = ["Июнь", "Июль", "Август"]
            lst_dates = ['06', '07', lst_date]
        elif lst_date == "09":
            labels = ["Июль", "Август", "Сентябрь"]
            lst_dates = ['07', '08', lst_date]
        elif lst_date == "10":
            labels = ["Август", "Сентябрь", "Октябрь"]
            lst_dates = ['08', '09', lst_date]
        elif lst_date == "11":
            labels = ["Сентябрь", "Октябрь", "Ноябрь"]
            lst_dates = ['09', '10', lst_date]
        elif lst_date == "12":
            labels = ["Октябрь", "Ноябрь", "Декабрь"]
            lst_dates = ['10', '11', lst_date]
        else:
            labels = ["Нет", "Нет", "Нет"]
            lst_dates = ['0', '0', "0"]

        data_graf = [0, 0, 0]
        for hs in list_history:
            if hs.date_operation.strftime("%m") in lst_dates[0]:
                data_graf[0] += 1
            elif hs.date_operation.strftime("%m") in lst_dates[1]:
                data_graf[1] += 1
            elif hs.date_operation.strftime("%m") in lst_dates[2]:
                data_graf[2] += 1

        last_activity = []
        all_activity = session.query(UserHistory).filter(UserHistory.user_id == user_id).all()
        user_info = session.query(Users).filter(Users.id == user_id).first()
        for i in range(-1, -7, -1):
            ds_info = session.query(Datasets).filter(Datasets.id == all_activity[i].dataset_id).first()
            x = {
                "nickname": user_info.login,
                "image_path": user_info.image_path,
                "text_label": all_activity[i].type_operation + " датасет \"" + ds_info.name + "\"",
                "data_label": all_activity[i].date_operation.strftime("%d.%m.%Y")
            }
            last_activity.append(x)

        response_json = {
            "panels": {
                "all_memory": count_memory,
                "count_ds": len(list_datasets),
                "count_download": len(list_history),
                "count_history": len(all_activity),
            },
            "graf": {
                "labels": labels,
                "datasets": [
                    {
                        "label": 'Количество загруженных датасетов',
                        "data": data_graf,
                        "backgroundColor": ["#7000e1", "#FC8800", "#00B0E8"],
                        "borderWidth": 0
                    }
                ]
            },
            "last_activity": last_activity,
        }
        self.logger.debug(f"Get dashboard: {response_json}")
        return response_json

    def get_datasets(self):
        session = create_session()
        list_datasets = session.query(Datasets).filter(Datasets.is_deleted == False).all()
        ls_ds = []
        for ds in list_datasets:
            x = {
                "ds_id": ds.id,
                "name": ds.name,
                "date_load": ds.date_load.strftime("%H:%M:%S %d.%m.%Y")
            }
            ls_ds.append(x)
        response_json = {
            "datasets": ls_ds,
        }
        self.logger.debug(f"Get datasets: {response_json}")
        return response_json

    def delete_dataset(self, dataset_id):
        session = create_session()
        ds = session.query(Datasets).filter(Datasets.id == dataset_id).first()
        ds.is_deleted = True
        new_history = UserHistory(
            user_id=ds.user_id,
            dataset_id=ds.user_id,
            type_operation="Удалил",
        )
        session.add(new_history)
        session.commit()
        self.logger.debug(f"Dataset deleted: {dataset_id}")

    def get_path_dataset(self, dataset_id, user_id):
        session = create_session()
        ds = session.query(Datasets).filter(Datasets.id == dataset_id).first()
        self.logger.debug(f"Dataset path: {ds.file_path}")
        new_history = UserHistory(
            user_id=user_id,
            dataset_id=ds.id,
            type_operation="Скачал"
        )
        session.add(new_history)
        session.commit()
        return ds.file_path

    def add_dataset(self, user_id, name_file, new_name, count_memory):
        session = create_session()
        new_dataset = Datasets(
            name=name_file,
            file_path=new_name,
            memory_used=count_memory,
            user_id=user_id,
            is_deleted=False
        )
        session.add(new_dataset)
        session.commit()
        new_history = UserHistory(
            user_id=user_id,
            dataset_id=new_dataset.id,
            type_operation="Загрузил"
        )
        session.add(new_history)
        session.commit()
        self.logger.debug(f"Add new dataset: {name_file}")

    def get_profile(self, user_id):
        session = create_session()

        last_activity = []
        all_activity = session.query(UserHistory).filter(UserHistory.user_id == user_id).all()
        user_info = session.query(Users).filter(Users.id == user_id).first()
        if all_activity:
            for i in range(-1, -len(all_activity) - 1, -1):
                ds_info = session.query(Datasets).filter(Datasets.id == all_activity[i].dataset_id).first()
                x = {
                    "nickname": user_info.login,
                    "image_path": user_info.image_path,
                    "text_label": all_activity[i].type_operation + " датасет \"" + ds_info.name + "\"",
                    "data_label": all_activity[i].date_operation.strftime("%d.%m.%Y")
                }
                last_activity.append(x)

        response_json = {
            "user_info": {
                "login": user_info.login,
                "email": user_info.email,
                "password": user_info.password,
                "image_path": user_info.image_path,
            },
            "user_activity": last_activity
        }
        self.logger.debug(f"Get datasets: {response_json}")
        return response_json

    def update_user(self, user_id, login, password, image_path):
        session = create_session()

        user_info = session.query(Users).filter(Users.id == user_id).first()
        user_info.login = login
        user_info.password = password
        user_info.image_path = image_path
        session.commit()
        self.logger.debug(f"User update: {user_id}")
